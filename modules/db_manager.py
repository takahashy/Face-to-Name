'''
db_manager.py

This module is used to manage the database using MySQL. 
The database connection details are defined in the .env file. 
Database contains a Users table that stores the names and faces of the users.
'''

import mysql.connector 
import os
import sys
import numpy as np
from typing import List
from dotenv import load_dotenv

load_dotenv()

class DBManager:

    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                port = int(os.getenv("DB_PORT")),
                database = os.getenv("DB_NAME"),
                passwd = os.getenv("DB_PASS")
            )

            self.cursor = self.db.cursor()

        except Exception as e:
            print(f"DB ERROR: Failed to connect to database: {e}")
            sys.exit(1)


    def createTable(self):
        self.__createPersonsTable()
        self.__createPhotosTable()        


    def insertFaces(self, name: str, face_paths: List[str], embeddings: List[np.ndarray]):
        id = self.__selectPerson(name)
        person_id = id if id != -1 else self.__insertPerson(name) 
        self.__insertPhotos(person_id, face_paths, embeddings)

        
    def fetchAllFaces(self):
        """
        get all the names, faces, and embeddings in the database
        """
        try:
            self.cursor.execute("""
                SELECT 
                    p.name, 
                    ph.face_path,
                    ph.embedding
                FROM Persons p
                INNER JOIN Photos ph ON p.id=ph.person_id;
            """)
            rows = self.cursor.fetchall()
        except Exception as e:
            print(f"DB ERROR: Failed to fetch data from Persons table: {e}")

        names, face_paths, embeddings = [], [], []
        for row in rows:
            names.append(row[0])
            face_paths.append(row[1])
            embeddings.append(np.frombuffer(row[2]))

        return names, face_paths, embeddings
    

    def getFacesOfName(self, name: str):
        """
        if the name is in the database return the paths to the images
        """
        id = self.__selectPerson(name)
        if id == -1:
            print(f"USER ERROR: `{name}` is not in database")
            return None
        
        try:
            query = "SELECT face_path, embedding FROM Photos WHERE person_id = %s;"
            self.cursor.execute(query, (id,))
            rows = self.cursor.fetchall()
            return [(row[0], np.frombuffer(row[1])) for row in rows]
        
        except Exception as e:
            print(f"DB ERROR: Failed to fetch data from Photos table: {e}")
        

    def close(self):
        try:
            if self.db and self.db.is_connected():
                self.cursor.close()
                self.db.close()
        except Exception as e:
            print(f"DB ERROR: Failed to close database: {e}")


    ### private methods
    def __createPersonsTable(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Persons (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
            """)
        except Exception as e:
            print(f"DB ERROR: Failed to create Persons table: {e}")
            sys.exit(1)


    # instead of storing the images, storing path to the images and embeddings 
    # leads to less memory usage and faster processing 
    def __createPhotosTable(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Photos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    person_id INT NOT NULL,
                    face_path VARCHAR(255) NOT NULL,
                    embedding BLOB NOT NULL,
                    FOREIGN KEY (person_id) REFERENCES Persons(id),
                    CONSTRAINT new_face UNIQUE (person_id, face_path)
                );
            """)
        except Exception as e:
            print(f"DB ERROR: Failed to create Photos table: {e}")
            sys.exit(1)


    def __selectPerson(self, name: str):
        try:
            query = "SELECT id FROM Persons WHERE name = %s;"
            self.cursor.execute(query, (name.lower(),))
            person_id = self.cursor.fetchone()

            if person_id:
                return person_id[0]
            else:
                return -1
            
        except Exception as e:
            print(f"DB ERROR: Failed to get user from Persons table: {e}")


    def __insertPerson(self, name: str):
        try:
            query = "INSERT INTO Persons (name) VALUES (%s);"
            self.cursor.execute(query, (name.lower(),))
            self.db.commit()
            return self.cursor.lastrowid
        
        except Exception as e:
            print(f"DB ERROR: Failed to insert new user into Persons table: {e}")


    def __insertPhotos(self, person_id: int, face_paths: List[str], embeddings: List[np.ndarray]):
        try:
            query = "INSERT IGNORE INTO Photos (person_id, face_path, embedding) VALUES (%s, %s, %s);"
            photos = [(person_id, face_path, embedding.tobytes()) for face_path, embedding in zip(face_paths, embeddings)]
            self.cursor.executemany(query, photos)
            self.db.commit()
        except Exception as e:  
            print(f"DB ERROR: Failed to insert new images into Photos table: {e}")


    def __clearTables(self):
        try:
            self.cursor.execute("DELETE FROM Photos")
            self.cursor.execute("DELETE FROM Persons")
            self.db.commit()
        except Exception as e:
            print(f"DB ERROR: Failed to clear tables: {e}")

    def __dropTables(self):
        try:
            self.cursor.execute("DROP TABLE Photos")
            self.cursor.execute("DROP TABLE Persons")
            self.db.commit()
        except Exception as e:
            print(f"DB ERROR: Failed to drop tables: {e}")