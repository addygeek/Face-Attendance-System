"""
Train Face Recognition Embeddings

This script processes all images in ml_model/data/ and generates embeddings
for face recognition. It saves the embeddings to web_app/embeddings/.

Usage:
    .venv311\Scripts\python.exe train_embeddings.py
"""

import os
import cv2
import numpy as np
import json
import mediapipe as mp
from datetime import datetime
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / 'ml_model' / 'data'
EMBEDDINGS_DIR = BASE_DIR / 'web_app' / 'embeddings'

# Ensure output directory exists
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# MediaPipe setup
mp_mesh = mp.solutions.face_mesh

def extract_embedding(image_path):
    """Extract face embedding from an image file."""
    img = cv2.imread(str(image_path))
    if img is None:
        return None
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    with mp_mesh.FaceMesh(
        static_image_mode=True,
        refine_landmarks=True,
        max_num_faces=1,
        min_detection_confidence=0.5
    ) as face_mesh:
        results = face_mesh.process(img_rgb)
        
        if not results.multi_face_landmarks:
            return None
        
        landmarks = results.multi_face_landmarks[0].landmark
        
        # 1. Raw landmarks
        raw = []
        for lm in landmarks:
            raw.extend([lm.x, lm.y, lm.z])
        raw = np.array(raw, dtype=np.float32)
        
        # 2. Derived features (distances between key points)
        def dist(i1, i2):
            p1 = landmarks[i1]
            p2 = landmarks[i2]
            return np.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)
        
        KP = {"leftEye": 33, "rightEye": 263, "nose": 1, "chin": 152, "leftMouth": 61, "rightMouth": 291}
        derived = [
            dist(KP["leftEye"], KP["rightEye"]), dist(KP["leftEye"], KP["nose"]),
            dist(KP["rightEye"], KP["nose"]), dist(KP["nose"], KP["chin"]),
            dist(KP["leftMouth"], KP["rightMouth"]), dist(KP["leftEye"], KP["chin"]),
            dist(KP["rightEye"], KP["chin"])
        ]
        derived = np.array(derived, dtype=np.float32)
        
        # 3. Normalize
        raw_norm = np.linalg.norm(raw)
        if raw_norm > 0:
            raw = raw / raw_norm
        der_norm = np.linalg.norm(derived)
        if der_norm > 0:
            derived = derived / der_norm
        
        return np.concatenate((raw, derived))

def train_person(person_name, person_dir):
    """Train embeddings for a single person from their image directory."""
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(person_dir.glob(ext))
    
    if not image_files:
        print(f"  ⚠ No images found for {person_name}")
        return None
    
    print(f"  Processing {len(image_files)} images...")
    
    embeddings = []
    for img_path in image_files:
        emb = extract_embedding(img_path)
        if emb is not None:
            embeddings.append(emb)
            print(f"    ✓ {img_path.name}")
        else:
            print(f"    ✗ {img_path.name} (no face detected)")
    
    if not embeddings:
        print(f"  ⚠ No valid faces found for {person_name}")
        return None
    
    # Average all embeddings
    avg_embedding = np.mean(embeddings, axis=0)
    
    # Save to JSON
    output_file = EMBEDDINGS_DIR / f"{person_name}_embedding.json"
    data = {
        "name": person_name,
        "embedding": avg_embedding.tolist(),
        "saved_at": datetime.utcnow().isoformat(),
        "num_images": len(embeddings)
    }
    
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"  ✓ Saved embedding from {len(embeddings)} images to {output_file.name}")
    return avg_embedding

def main():
    print("="*60)
    print("Face Recognition Training Script")
    print("="*60)
    print(f"Data directory: {DATA_DIR}")
    print(f"Output directory: {EMBEDDINGS_DIR}")
    print()
    
    if not DATA_DIR.exists():
        print(f"ERROR: Data directory not found: {DATA_DIR}")
        return
    
    # Find all person directories
    person_dirs = [d for d in DATA_DIR.iterdir() if d.is_dir()]
    
    if not person_dirs:
        print(f"ERROR: No person directories found in {DATA_DIR}")
        return
    
    print(f"Found {len(person_dirs)} people to train:")
    for d in person_dirs:
        print(f"  - {d.name}")
    print()
    
    # Train each person
    trained_count = 0
    for person_dir in person_dirs:
        person_name = person_dir.name
        print(f"Training: {person_name}")
        
        result = train_person(person_name, person_dir)
        if result is not None:
            trained_count += 1
        print()
    
    print("="*60)
    print(f"Training complete! Successfully trained {trained_count}/{len(person_dirs)} people.")
    print("="*60)

if __name__ == "__main__":
    main()
