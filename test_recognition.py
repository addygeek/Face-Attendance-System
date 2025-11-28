"""
Test Face Recognition System

This script tests the face recognition by:
1. Loading embeddings from web_app/embeddings/
2. Testing with sample images from ml_model/data/
3. Verifying recognition accuracy

Usage:
    .venv311\Scripts\python.exe test_recognition.py
"""

import os
import sys
import cv2
import numpy as np
import json
from pathlib import Path

# Add ml_model to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'ml_model'))

from utils.helpers import load_embeddings, cosine_similarity
from utils.extract_embedding import get_embedding

def test_recognition():
    print("="*60)
    print("Face Recognition Test")
    print("="*60)
    
    # Load embeddings
    print("\n1. Loading embeddings...")
    embeddings = load_embeddings()
    
    if not embeddings:
        print("   ✗ No embeddings found!")
        print("   Run: .venv311\\Scripts\\python.exe train_embeddings.py")
        return False
    
    print(f"   ✓ Loaded {len(embeddings)} embeddings:")
    for name in embeddings.keys():
        print(f"     - {name}")
    
    # Test with sample images
    print("\n2. Testing with sample images...")
    data_dir = Path(__file__).parent / 'ml_model' / 'data'
    
    if not data_dir.exists():
        print(f"   ✗ Data directory not found: {data_dir}")
        return False
    
    test_results = []
    threshold = 0.5
    
    for person_dir in data_dir.iterdir():
        if not person_dir.is_dir():
            continue
        
        person_name = person_dir.name
        image_files = list(person_dir.glob('*.jpg')) + list(person_dir.glob('*.png'))
        
        if not image_files:
            continue
        
        # Test with first image
        test_image = image_files[0]
        print(f"\n   Testing: {person_name} ({test_image.name})")
        
        # Extract embedding
        test_emb = get_embedding(str(test_image))
        
        if test_emb is None:
            print(f"     ✗ No face detected in image")
            test_results.append({'name': person_name, 'status': 'no_face'})
            continue
        
        # Compare with all embeddings
        best_match = None
        best_sim = -1
        
        for name, known_emb in embeddings.items():
            sim = cosine_similarity(test_emb, known_emb)
            if sim > best_sim:
                best_sim = sim
                best_match = name
        
        # Check result
        is_correct = best_match == person_name
        is_recognized = best_sim >= threshold
        
        if is_correct and is_recognized:
            print(f"     ✓ PASS: Recognized as {best_match} (similarity: {best_sim:.3f})")
            test_results.append({'name': person_name, 'status': 'pass', 'similarity': best_sim})
        elif is_recognized:
            print(f"     ✗ FAIL: Recognized as {best_match} instead of {person_name} (similarity: {best_sim:.3f})")
            test_results.append({'name': person_name, 'status': 'wrong_match', 'similarity': best_sim})
        else:
            print(f"     ⚠ WARNING: Not recognized (best: {best_match} with {best_sim:.3f}, threshold: {threshold})")
            test_results.append({'name': person_name, 'status': 'not_recognized', 'similarity': best_sim})
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for r in test_results if r['status'] == 'pass')
    total = len(test_results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All tests passed! Face recognition is working correctly.")
        return True
    else:
        print("\n⚠ Some tests failed. You may need to:")
        print("  1. Retrain embeddings: .venv311\\Scripts\\python.exe train_embeddings.py")
        print("  2. Adjust threshold in ml_model/video_processors.py")
        print("  3. Ensure training images are clear and well-lit")
        return False

if __name__ == "__main__":
    success = test_recognition()
    sys.exit(0 if success else 1)
