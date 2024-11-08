'''
getFaces.py

Show all the images of a person in the database
'''

import cv2
import numpy as np
from modules.utils import processImage
from modules.db_manager import DBManager


def main():
    db_manager = DBManager()
    name = input("Enter the name of the person: ").strip()

    images = db_manager.getFacesOfName(name)
    
    if images:
        count = 1
        for path, embedding in images:
            image_cv2 = cv2.imread(path)
            locations, embeddings = processImage(path)

            for face_location, face_embedding in zip(locations, embeddings):
                if np.array_equal(face_embedding, embedding):
                    top, right, bottom, left = face_location
                    cv2.rectangle(image_cv2, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.imshow(name + " #" + str(count), image_cv2)
                    count += 1

        cv2.waitKey(0)
        cv2.destroyAllWindows()


    db_manager.close()


if __name__ == "__main__":
    main()