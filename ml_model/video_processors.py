import cv2
import numpy as np
import mediapipe as mp
import av
from datetime import datetime
from streamlit_webrtc import VideoTransformerBase
from .utils.helpers import load_embeddings, log_attendance, cosine_similarity

# Mediapipe Setup
mp_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

class AttendanceVideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.embeddings = load_embeddings()
        self.threshold = 0.5 # Adjusted threshold
        self.last_log_time = {}

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        with mp_mesh.FaceMesh(
            static_image_mode=False,
            refine_landmarks=True,
            max_num_faces=4,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:
            results = face_mesh.process(img_rgb)
            
            if results.multi_face_landmarks:
                for landmarks in results.multi_face_landmarks:
                    # Extract embedding logic
                    raw = []
                    for lm in landmarks.landmark:
                        raw.extend([lm.x, lm.y, lm.z])
                    raw = np.array(raw, dtype=np.float32)
                    
                    lm_list = landmarks.landmark
                    def dist(i1, i2):
                        p1 = lm_list[i1]
                        p2 = lm_list[i2]
                        return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
                    
                    KP = { "leftEye": 33, "rightEye": 263, "nose": 1, "chin": 152, "leftMouth": 61, "rightMouth": 291 }
                    derived = [
                        dist(KP["leftEye"], KP["rightEye"]), dist(KP["leftEye"], KP["nose"]),
                        dist(KP["rightEye"], KP["nose"]), dist(KP["nose"], KP["chin"]),
                        dist(KP["leftMouth"], KP["rightMouth"]), dist(KP["leftEye"], KP["chin"]),
                        dist(KP["rightEye"], KP["chin"])
                    ]
                    derived = np.array(derived, dtype=np.float32)
                    
                    raw_norm = np.linalg.norm(raw)
                    if raw_norm > 0: raw = raw / raw_norm
                    der_norm = np.linalg.norm(derived)
                    if der_norm > 0: derived = derived / der_norm
                    
                    emb = np.concatenate((raw, derived))
                    
                    # Identify
                    best_name = "Unknown"
                    best_sim = -1
                    
                    if self.embeddings:
                        for name, known_emb in self.embeddings.items():
                            sim = cosine_similarity(emb, known_emb)
                            if sim > best_sim:
                                best_sim = sim
                                best_name = name
                    
                    color = (0, 0, 255)
                    if best_sim >= self.threshold:
                        color = (0, 255, 0)
                        # Log attendance
                        now = datetime.now()
                        last_time = self.last_log_time.get(best_name)
                        if not last_time or (now - last_time).total_seconds() > 30:
                            self.last_log_time[best_name] = now
                            print(f"LOGGING: {best_name} ({best_sim})")
                            try:
                                log_attendance(best_name, best_sim)
                            except Exception as e:
                                print(f"Logging error: {e}")

                    else:
                        best_name = "Unknown"

                    # Draw
                    h, w, c = img.shape
                    x_min, x_max = w, 0
                    y_min, y_max = h, 0
                    for lm in landmarks.landmark:
                        x, y = int(lm.x * w), int(lm.y * h)
                        if x < x_min: x_min = x
                        if x > x_max: x_max = x
                        if y < y_min: y_min = y
                        if y > y_max: y_max = y
                    
                    cv2.rectangle(img, (x_min, y_min), (x_max, y_max), color, 2)
                    cv2.putText(img, f"{best_name} {best_sim:.2f}", (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")
