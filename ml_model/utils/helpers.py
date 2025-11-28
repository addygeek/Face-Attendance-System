import os
import json
import numpy as np
from datetime import datetime
import streamlit as st

# Constants
# Assuming this file is in ml_model/utils/helpers.py
# BASE_DIR should be the root of the project (d:\PROGRAMING\7th sem 7\face\face_detection_app)
# __file__ is .../ml_model/utils/helpers.py
# os.path.dirname(__file__) is .../ml_model/utils
# .../.. is .../ml_model
# .../../.. is root

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
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

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
