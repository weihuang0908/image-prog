import os

class BaseConfig(object):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
	HISTORY_CSV_PATH="res/data/beijing.csv"
	conf=0
	#hpc lab
	if conf == 0:
		MONGO_ADDRESS = "10.0.1.119"
		MONGO_PORT = 27017
		MONGO_USER = "admin"
		MONGO_PASS = "hpc1234"
	#home
	if conf ==1:
		MONGO_ADDRESS = "0.0.0.0"
		MONGO_PORT = 27017
		MONGO_USER = "admin"
		MONGO_PASS = "hpc1234"