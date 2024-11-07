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

def main(arg):
    """
    should read a name directory or all directories
    """
    db_manager = DBManager()
    image_paths, embeddings = [], []

    if arg == "all":
        for subdir in DATA_DIR.iterdir():
            image_paths, embeddings = [], []
            name = subdir.name
            if subdir.is_dir() and name != "test":
                print(f"----Reading {name}----")
                for image in subdir.iterdir():
                    if imageExists(image):
                        embedding = processImage(str(image))[1]

                        if embedding:
                            image_paths.append(str(image))
                            embeddings += embedding
                        else:
                            print(f"IMAGE WARNING: Cannot find facial features in {image}")
                    
                    print(f"Processing {image.name}...")
                db_manager.insertFaces(name, image_paths, embeddings)
                print()

    elif isDirectory("data/" + arg):
        for image in (DATA_DIR / arg).iterdir():
            if imageExists(image):
                embedding = processImage(str(image))[1]

                if embedding:
                    image_paths.append(str(image))
                    embeddings += embedding
                else:
                    print(f"IMAGE WARNING: Cannot find facial features in {image}")
            
            print(f"Processing {image.name}...")
        db_manager.insertFaces(arg, image_paths, embeddings)

    else:
        print("PATH ERROR: `{image_file}` does not exist") 
        sys.exit(1)


    print(f"\33[92mDone!\033[0m")
    db_manager.close()

if __name__ == "__main__":
    if len(sys.argv) != 2 :
        print("USAGE: python3 add_new_faces.py [ directory | 'all']")
        sys.exit(1)

    main(sys.argv[1])