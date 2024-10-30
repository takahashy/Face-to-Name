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

print(load_dotenv())

class DBManager:
    def __init__(self):
        try:
            self.db = mysql.connector.connect(
                host = os.getenv("DB_HOST"),
                user = os.getenv("DB_USER"),
                port = int(os.getenv("DB_PORT")),
                passwd = os.getenv("DB_PASS")
            )
            self.cursor = self.db.cursor()

        except Exception as e:
            print(os.getenv("DB_HOST"))
            print(f"ERROR: Failed to connect to database: {e}")
            sys.exit(1)


    def createDatabase(self):
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS face_recognition;")
            self.cursor.execute("USE face_recognition;")
        except Exception as e:
            print(f"ERROR: Failed to create database: {e}")
            sys.exit(1)


    def createTable(self):
        self.__createPersonsTable()
        self.__createPhotosTable()        


    def insertData(self, name: str, face_paths: List[str], embeddings: List[np.ndarray]):
        # insert just the name to Persons table
        try:
            sql = "INSERT INTO Persons (name) VALUES (%s);"
            self.cursor.execute(sql, (name,))
        except Exception as e:
            print(f"ERROR: Failed to insert data into Persons table: {e}")

        person_id = self.cursor.lastrowid

        # insert each photo path and embedding to the Photos table
        try:
            sql = "INSERT INTO Photos (person_id, face_path, embedding) VALUES (%s, %s, %s);"
            for face_path, embedding in zip(face_paths, embeddings):
                self.cursor.execute(sql, (person_id, face_path, embedding.tobytes()))
            self.db.commit()
        except Exception as e:
            print(f"ERROR: Failed to insert data into Photos table: {e}")


    def fetchData(self):
        try:
            self.cursor.execute("""
                SELECT 
                    p.name, 
                    ph.face_path,
                    ph.embedding
                FROM Persons p
                INNER JOIN Photos ph ON p.id=ph.person_id;
            """)
            print(self.cursor.fetchall())
        except Exception as e:
            print(f"ERROR: Failed to fetch data from Persons table: {e}")
            sys.exit(1)


    def close(self):
        try:
            self.__clearTables()
            self.cursor.close()
            self.db.close()
        except Exception as e:
            print(f"ERROR: Failed to close database: {e}")


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
            print(f"ERROR: Failed to create Persons table: {e}")
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
                    FOREIGN KEY (person_id) REFERENCES Persons(id)
                );
            """)
        except Exception as e:
            print(f"ERROR: Failed to create Photos table: {e}")
            sys.exit(1)


    def __clearTables(self):
        try:
            self.cursor.execute("DELETE FROM Persons")
            self.cursor.execute("DELETE FROM Photos")
        except Exception as e:
            print(f"ERROR: Failed to clear tables: {e}")
