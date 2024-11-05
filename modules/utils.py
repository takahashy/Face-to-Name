'''
utils.py

helper functions
'''

import sys
from pathlib import Path

def directory_exists(directory: str) -> bool:
    return Path(directory).is_dir()

def file_exists(file_path: str) -> bool:
    return Path(file_path).is_file()
    
def image_exists(image_path: str) -> bool:
    if not file_exists(image_path):
        print(f"PATH ERROR: `{image_path}` file does not exist")
        sys.exit(1)
        
    file = Path(image_path)
    isImage = file.suffix == ".jpg" or file.suffix == ".png" or file.suffix == ".jpeg"
    return isImage