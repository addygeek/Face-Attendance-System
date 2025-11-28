import streamlit as st
import cv2
import numpy as np
import os
import json
import pandas as pd
from streamlit_webrtc import webrtc_streamer

# Import custom modules
from ml_model.utils.helpers import (
    load_embeddings, 
    save_embedding, 
    ATTENDANCE_FILE, 
    EMBEDDINGS_DIR
)
from ml_model.utils.extract_embedding import get_embedding as extract_embedding_from_file
from ml_model.video_processors import AttendanceVideoProcessor

# We need a helper to extract embedding from in-memory image for registration
# The existing utils/extract_embedding.py takes a file path.
# We should probably adapt it or just use the logic inline here for registration since it's simple.
# Or better, let's update extract_embedding.py to handle numpy arrays too.
# For now, I will implement a simple wrapper here or duplicate the logic for registration to keep it robust.
# Actually, I can use the logic from video_processors but that's inside a class.
# Let's just import the logic from helpers if I put it there? No, I didn't put extraction logic in helpers.
# I will add a simple extraction function here for registration using MediaPipe directly, similar to before.

import mediapipe as mp
mp_mesh = mp.solutions.face_mesh

def extract_embedding_registration(image):
    with mp_mesh.FaceMesh(
        static_image_mode=True,
        refine_landmarks=True,
        max_num_faces=1,
        min_detection_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(image)
        if not results.multi_face_landmarks:
            return None
        
        landmarks = results.multi_face_landmarks[0].landmark
        
        # 1. Raw
        raw = []
        for lm in landmarks:
            raw.extend([lm.x, lm.y, lm.z])
        raw = np.array(raw, dtype=np.float32)
        
        # 2. Derived
        def dist(i1, i2):
            p1 = landmarks[i1]
            p2 = landmarks[i2]
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
        
        return np.concatenate((raw, derived))


# Set page config
st.set_page_config(page_title="Face Attendance System", layout="wide", page_icon="📸")

# --- UI Layout ---

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home (Attendance)", "Register Face", "View Logs"])

if page == "Home (Attendance)":
    st.title("📸 Face Attendance System")
    st.write("Real-time face recognition and attendance logging.")
    
    # WebRTC Streamer
    webrtc_streamer(
        key="attendance", 
        video_processor_factory=AttendanceVideoProcessor, 
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

elif page == "Register Face":
    st.title("👤 Register New Face")
    
    name = st.text_input("Enter Name")
    
    img_file = st.camera_input("Take a picture")
    
    if img_file is not None and name:
        if st.button("Save Face"):
            bytes_data = img_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            
            embedding = extract_embedding_registration(rgb_img)
            
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
