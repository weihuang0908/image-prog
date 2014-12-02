import pymongo
class MongoClient(object):
	def __init__(self, host, port, username, password):
		self.db = pymongo.Connection(host, port)["pm25"]
		self.db.authenticate(username, password)
		self.col_1 = self.db['beijing']
	def findOne_from_col_1(self):
		return self.col_1.find_one()
	def find_from_col_1(self,query=None):
		return self.col_1.find(query)
	def insert_into_col_1(self,data):
		_id = self.col_1.insert(data)
		return str(_id)
	def delete_repeat_records(self,indexList=None):
		#### db.beijing.ensureIndex({'time_point':1,"station_code":1}, {"unique": true, "dropDups": true})
		if indexList is None:
			indexList=[('time_point',1),('station_code',1)]
			self.col_1.ensureIndex(indexList,unique=True, dropDups=True,name="_time_station_index_")
	def update_time_format(self):
		query={"time_point":{"$regex":".*T.*Z"}}
		for item in self.find_from_col_1(query):
			time_point=item["time_point"]
			time_point=time_point[:-1].replace('T',' ')
			_id=item["_id"]
			self.col_1.update({"_id":_id},{"$set":{"time_point":time_point}})


