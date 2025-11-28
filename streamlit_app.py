import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import os
import json
import pandas as pd
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, WebRtcMode
import av

# Set page config
st.set_page_config(page_title="Face Attendance System", layout="wide", page_icon="📸")

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
EMBEDDINGS_DIR = os.path.join(BASE_DIR, 'web_app', 'embeddings')
ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.json')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

# Initialize attendance file
if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump({'records': [], 'next_id': 1}, f, indent=2)

# Mediapipe Setup
mp_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# --- Helper Functions ---

def load_embeddings():
    embeddings = {}
    if not os.path.exists(EMBEDDINGS_DIR):
        return embeddings
    
    for filename in os.listdir(EMBEDDINGS_DIR):
        if filename.endswith('_embedding.json'):
            name = filename.replace('_embedding.json', '')
            try:
                with open(os.path.join(EMBEDDINGS_DIR, filename), 'r') as f:
                    data = json.load(f)
                    embeddings[name] = np.array(data['embedding'], dtype=np.float32)
            except Exception as e:
                st.error(f"Error loading embedding for {name}: {e}")
    return embeddings

def save_embedding(name, embedding):
    filepath = os.path.join(EMBEDDINGS_DIR, f"{name}_embedding.json")
    data = {
        "name": name,
        "embedding": embedding.tolist(),
        "saved_at": datetime.utcnow().isoformat()
    }
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def log_attendance(name, confidence):
    try:
        with open(ATTENDANCE_FILE, 'r') as f:
            data = json.load(f)
    except:
        data = {'records': [], 'next_id': 1}
    
    now = datetime.now()
    # Check if already logged recently (e.g., last 1 minute)
    last_log = None
    for record in reversed(data['records']):
        if record['name'] == name:
            last_log = datetime.fromisoformat(record['timestamp'])
            break
            
    if last_log and (now - last_log).total_seconds() < 60:
        return False # Already logged recently

    record = {
        'id': data['next_id'],
        'name': name,
        'timestamp': now.isoformat(),
        'confidence': float(confidence),
        'created_at': now.isoformat(),
        'start_time': now.isoformat()
    }
    data['records'].append(record)
    data['next_id'] += 1
    
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    return True

def extract_embedding(image):
    # Image is already RGB from streamlit-webrtc or converted
    with mp_mesh.FaceMesh(
        static_image_mode=True,
        refine_landmarks=True,
        max_num_faces=1,
        min_detection_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(image)
        
        if not results.multi_face_landmarks:
            return None
            
        face = results.multi_face_landmarks[0]
        landmarks = face.landmark
        
        # 1. Raw Coordinates
        raw = []
        for lm in landmarks:
            raw.extend([lm.x, lm.y, lm.z])
        raw = np.array(raw, dtype=np.float32)
        
        # 2. Derived Features
        KP = {
            "leftEye": 33, "rightEye": 263, "nose": 1, "chin": 152,
            "leftMouth": 61, "rightMouth": 291
        }
        
        def dist(i1, i2):
            p1 = landmarks[i1]
            p2 = landmarks[i2]
            return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
            
        derived = [
            dist(KP["leftEye"], KP["rightEye"]),
            dist(KP["leftEye"], KP["nose"]),
            dist(KP["rightEye"], KP["nose"]),
            dist(KP["nose"], KP["chin"]),
            dist(KP["leftMouth"], KP["rightMouth"]),
            dist(KP["leftEye"], KP["chin"]),
            dist(KP["rightEye"], KP["chin"])
        ]
        derived = np.array(derived, dtype=np.float32)
        
        # 3. Normalization
        raw_norm = np.linalg.norm(raw)
        if raw_norm > 0: raw = raw / raw_norm
        
        der_norm = np.linalg.norm(derived)
        if der_norm > 0: derived = derived / der_norm
        
        # 4. Concatenate
        return np.concatenate((raw, derived))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# --- Video Processor ---

class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.embeddings = load_embeddings()
        self.threshold = 0.5 # Adjusted threshold, original JS was 0.1 but cosine sim usually higher
        # JS code used 0.1 threshold? That seems very low for cosine similarity unless vectors are not normalized well or different metric.
        # Let's stick to logic from JS: dot / (norm*norm). 
        # Wait, JS code: 
        # function cosine(a, b) { ... return dot / (Math.sqrt(na) * Math.sqrt(nb)); }
        # And THRESHOLD = 0.1;
        # If vectors are similar, cosine sim should be close to 1. 0.1 is very low. 
        # Maybe the embedding extraction produces vectors that are not very aligned?
        # I will use the same threshold as JS for consistency.
        self.threshold = 0.1 

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # We need to create a new FaceMesh instance here or reuse a global one?
        # Creating one per frame is expensive. But VideoProcessor runs in a separate thread.
        # Let's try to use a context manager inside or just one instance if possible.
        # For simplicity and performance, let's just use the one from helper but we need to be careful about thread safety.
        # Actually, `extract_embedding` creates a new FaceMesh every time. This is slow for real-time.
        # Let's optimize:
        
        with mp_mesh.FaceMesh(
            static_image_mode=False, # Optimized for video
            refine_landmarks=True,
            max_num_faces=4,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:
            results = face_mesh.process(img_rgb)
            
            if results.multi_face_landmarks:
                for landmarks in results.multi_face_landmarks:
                    # Draw landmarks
                    mp_drawing.draw_landmarks(
                        image=img,
                        landmark_list=landmarks,
                        connections=mp_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
                    
                    # Extract embedding (we need to adapt extract_embedding to take landmarks directly to avoid re-processing)
                    # But for now, let's just re-use the logic inside extract_embedding but adapted for landmarks object
                    
                    # ... (Logic from extract_embedding adapted for landmarks object)
                    # 1. Raw
                    raw = []
                    for lm in landmarks.landmark:
                        raw.extend([lm.x, lm.y, lm.z])
                    raw = np.array(raw, dtype=np.float32)
                    
                    # 2. Derived
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
                    
                    # 3. Norm
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
                    
                    color = (0, 0, 255) # Red
                    if best_sim >= self.threshold:
                        color = (0, 255, 0) # Green
                        # Log attendance (side effect in thread? might be risky but let's try)
                        # Ideally we pass this back to main thread, but for simple app:
                        # We can't easily call streamlit functions here.
                        # We can write to file though.
                        # To avoid file lock issues, maybe just print or use a queue?
                        # For now, let's just visualize.
                        pass
                    else:
                        best_name = "Unknown"

                    # Draw Box & Name
                    h, w, c = img.shape
                    cx, cy = int(landmarks.landmark[1].x * w), int(landmarks.landmark[1].y * h)
                    cv2.putText(img, f"{best_name} ({best_sim:.2f})", (cx - 50, cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- UI Layout ---

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home (Attendance)", "Register Face", "View Logs"])

if page == "Home (Attendance)":
    st.title("📸 Face Attendance System")
    st.write("Real-time face recognition and attendance logging.")
    
    # We need a way to log attendance from the video stream. 
    # Since VideoProcessor runs in a separate process/thread, we can't directly update UI or safely write to shared file without care.
    # However, `streamlit-webrtc` allows callbacks. 
    # For this MVP, we will do the recognition in the `recv` method (VideoProcessor) and maybe write to a queue or just write to file carefully.
    # The `log_attendance` function uses a simple file append, which might have race conditions if multiple threads write, but for single user it's fine.
    
    # Let's redefine VideoProcessor to handle logging
    class AttendanceVideoProcessor(VideoTransformerBase):
        def __init__(self):
            self.embeddings = load_embeddings()
            self.threshold = 0.1
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
                        # Extract embedding logic (duplicated for now to avoid pickling issues with external funcs)
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
                                sim = np.dot(emb, known_emb) / (np.linalg.norm(emb) * np.linalg.norm(known_emb))
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
                                # We can't easily call the global log_attendance here because of file I/O in loop
                                # But let's try to just print for now, or use a simple append
                                # Ideally we'd use a queue. 
                                # For simplicity in this script, we will just print to console which shows in server logs
                                print(f"LOGGING: {best_name} ({best_sim})")
                                # We can try to write to file directly here
                                try:
                                    # Read-Modify-Write is risky here but acceptable for MVP
                                    # Using a separate lock would be better
                                    pass 
                                    # Actually, let's just visualize it. The user can see "Green" box.
                                    # To truly log, we need to handle it. 
                                    # Let's call the global function, hoping no race condition.
                                    log_attendance(best_name, best_sim)
                                except Exception as e:
                                    print(f"Logging error: {e}")

                        else:
                            best_name = "Unknown"

                        # Draw
                        h, w, c = img.shape
                        # Bounding box approximation from landmarks
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

    webrtc_streamer(key="attendance", video_processor_factory=AttendanceVideoProcessor, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

elif page == "Register Face":
    st.title("👤 Register New Face")
    
    name = st.text_input("Enter Name")
    
    img_file = st.camera_input("Take a picture")
    
    if img_file is not None and name:
        if st.button("Save Face"):
            bytes_data = img_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            
            embedding = extract_embedding(rgb_img)
            
            if embedding is not None:
                save_embedding(name, embedding)
                st.success(f"Successfully registered {name}!")
            else:
                st.error("No face detected. Please try again.")

elif page == "View Logs":
    st.title("📊 Attendance Logs")
    
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as f:
            data = json.load(f)
        
        if data['records']:
            df = pd.DataFrame(data['records'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp', ascending=False)
            
            st.dataframe(df)
            
            if st.button("Refresh Logs"):
                st.rerun()
                
            if st.button("Clear Logs"):
                with open(ATTENDANCE_FILE, 'w') as f:
                    json.dump({'records': [], 'next_id': 1}, f, indent=2)
                st.success("Logs cleared!")
                st.rerun()
        else:
            st.info("No attendance records found.")
    else:
        st.info("Attendance file not found.")
