'''
add_new_faces.py

Given an image or images of a person or a group of people, 
this script adds the faces to the database. 
'''
import sys
from pathlib import Path
from modules.db_manager import DBManager
from modules.utils import isDirectory, imageExists, processImage

DATA_DIR = Path(__file__).parent.parent / "data"
DB_MANAGER = DBManager()

def iterateDir(dir: Path, name:str) -> None:
    """
    iterate through the images in the name directory and add them to database
    """
    image_paths, embeddings = [], []
    for image in dir.iterdir():
        if imageExists(image):
            embedding = processImage(str(image))[1]

            if embedding:
                image_paths.append(str(image))
                embeddings += embedding
            else:
                print(f"IMAGE WARNING: Cannot find facial features in {image}")
        
        print(f"Processing {image.name}...")
    DB_MANAGER.insertFaces(name, image_paths, embeddings)
    print()

def main(arg):
    """
    reads from a name directory or all directories in the data directory
    adds new faces to the database.
    """
    if arg == "all":
        for subdir in DATA_DIR.iterdir():
            name = subdir.name
            if subdir.is_dir():
                print(f"----Reading {name}----")
                iterateDir(subdir, name)

    elif isDirectory("data/" + arg):
        iterateDir(DATA_DIR / arg, arg)

    else:
        print("PATH ERROR: `{image_file}` does not exist") 
        sys.exit(1)

    print(f"\33[92mDone!\033[0m")
    DB_MANAGER.close()


if __name__ == "__main__":
    if len(sys.argv) != 2 :
        print("USAGE: python3 add_new_faces.py [ directory | 'all']")
        sys.exit(1)

    main(sys.argv[1])