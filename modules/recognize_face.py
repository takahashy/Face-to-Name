'''
recognize_face.py

This module is used to process the face images, extract the embeddings, and recognize the faces.
The image to be processed is given either as a user prompt or from the data directory.
If the person is not in the database, 
'''

import cv2
import numpy as np
import face_recognition
from typing import Tuple, List
from modules.utils import processImage
from modules.db_manager import DBManager

# cv2 image
SECONDS = 2
FONT_SCALE = 0.7
RED   = (0, 0, 255)
GREEN = (0, 255, 0)
BLUE  = (255, 0, 0)

# face recognition
TOLERANCE = 0.35

class RecognizeFace:

    def __init__(self):
        """
        users is a dictionary where key is embeddings and value is (name, face_path)
        """
        self.db = DBManager()
        self.names, self.face_paths, self.embeddings = self.db.fetchFaces()

    def recognizeFaces(self, image_path: str) -> List[Tuple]:
        """
        Given a path to an image, return list of unrecognized faces 
        """
        face_locations, face_embeddings = processImage(image_path)
        unknown_faces, known_faces = [], []

        image_cv2 = cv2.imread(image_path)

        for (top, right, bottom, left), embedding in zip(face_locations, face_embeddings):
            matches = face_recognition.compare_faces(self.embeddings, embedding, TOLERANCE)
            distances = face_recognition.face_distance(self.embeddings, embedding)
            best_match_index = np.argmin(distances) if len(distances) != 0 else -1

            name = "Unknown"
            if matches and matches[best_match_index]:
                name = self.names[best_match_index]

            if name == "Unknown":
                unknown_faces.append(((top, right, bottom, left), embedding))
            else:
                known_faces.append((name, (top, right, bottom, left), embedding))
                
            color = GREEN if name != "Unknown" else RED
            cv2.rectangle(image_cv2, (left, bottom), (right, top), color, 2)
            cv2.putText(image_cv2, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, color, 2)

        self.showImage(image_cv2)
        return unknown_faces, known_faces


    def checkFaces(self, unknown_faces: List[Tuple], known_faces: List[Tuple], image_path: str) -> List[Tuple]:        
        """
        Ask the name for each unknown and incorrect faces. 
        Add those names and faces to the database.
        """
        unrecognized_faces = []

        if unknown_faces:
            for (top, right, bottom, left), embedding in unknown_faces:
                image_cv2 = cv2.imread(image_path)
                cv2.rectangle(image_cv2, (left, bottom), (right, top), BLUE, 3)
                self.showImage(image_cv2, SECONDS)

                name = input("Enter the name of the person: ").strip()
                unrecognized_faces.append((name, embedding))

        if input("\nAre the known names correct? (y/n) ").lower()[0] != "y":
            for name, (top, right, bottom, left), embedding in known_faces:
                image_cv2 = cv2.imread(image_path)
                cv2.rectangle(image_cv2, (left, bottom), (right, top), RED, 3)
                cv2.putText(image_cv2, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, FONT_SCALE, RED, )
                self.showImage(image_cv2, SECONDS)

                if input(f"Is {name} correct? (y/n) ").lower() == "n":
                    name = input("Enter the name of the person: ").strip()
                    unrecognized_faces.append((name, embedding))
                print()
        
        self.addNewFaces(unrecognized_faces, image_path)
        print("\033[92mDone!\033[0m")


    def addNewFaces(self, unrecognized_faces: List[Tuple], image_path: str) -> None:
        """
        Given a list of unrecognized faces and path to image
        add them to the database. 
        """
        for name, embedding in unrecognized_faces:
            self.db.insertFaces(name, [image_path], [embedding])
            self.names.append(name) if name not in self.names else None
            self.face_paths.append(image_path)
            self.embeddings.append(embedding)  


    def showImage(self, image: cv2, mili_sec=0) -> None:
        cv2.imshow("Recognizing Faces", image)
        cv2.waitKey(mili_sec * 1000)
        cv2.destroyAllWindows()