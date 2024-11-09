'''
db_init.py

create the tables in the database
'''

from modules.db_manager import DBManager


def init_db():
    db = DBManager()
    db.createTable()
    db.close()
    
if __name__ == "__main__":
    init_db()