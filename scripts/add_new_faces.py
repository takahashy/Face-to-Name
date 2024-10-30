from modules.db_manager import DBManager
import numpy as np

dbm = DBManager()
dbm.insertData("new_person", ["path1", "path2"], [np.array([1, 2, 3]), np.array([4, 5, 6])])
dbm.fetchData()
dbm.close()