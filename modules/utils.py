'''
utils.py

helper functions
'''

import sys
import numpy as np
import face_recognition
from pathlib import Path
from typing import List, Tuple


def isDirectory(directory: str) -> bool:
    return Path(directory).is_dir()

def isFile(file_path: str) -> bool:
    return Path(file_path).is_file()
    
def imageExists(image_path: str) -> bool:
    if not isFile(image_path):
        print(f"PATH ERROR: `{image_path}` file does not exist")
        sys.exit(1)
        
    ext = Path(image_path).suffix.lower()
    isImage = ext == ".jpg" or ext == ".png" or ext == ".jpeg"
    return isImage

def processImage(image_path: str) -> Tuple[List[np.ndarray], List[np.ndarray]]:
    """
    Given a path to an image, return the location and embeddings 
    of each face in image
    """
    image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(image)
    face_embeddings = face_recognition.face_encodings(image, face_locations)
    return (face_locations, face_embeddings)