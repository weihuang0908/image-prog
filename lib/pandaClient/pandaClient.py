import pandas
class PandaClient(object):
	"""read csv"""
	def __init__(self):
		super(PandaClient, self).__init__()
	def read_csv(self,filePath):
		data=[]
		# names=["time_point","type", "area", "position_name", "AQI", "quality","Level", "pm2_5","pm2_5_24h"\
		# "pm10" , "pm10_24h","co" ,"co_24h","no2","no2_24h","o3","o3_24h","o3_8h","o3_8h_24h" ,"so2" ,"so2_24h", "Real_AQI"]
		self.csv=pd.read_csv(filePath,parse_dates=True,index_col=0,header=0)

# slice data example :
# In [191]: csv["2014-10-24 14:00:00"][["type","PM2.5"]]
# Out[191]:
#                     type  PM2.5
# time
# 2014-10-24 14:00:00   国控    268
# 2014-10-24 14:00:00  非国控    294
