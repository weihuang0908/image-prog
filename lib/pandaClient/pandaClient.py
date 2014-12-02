import panda
class PandaClient(object):
	"""read csv"""
	def __init__(self):
		super(PandaClient, self).__init__()
	def read_csv(self,filePath):
		data=[]
		names=["time_point","type", "area", "position_name", "AQI", "quality","Level", "pm2_5","pm2_5_24h"\
		"pm10" , "pm10_24h","co" ,"co_24h","no2","no2_24h","o3","o3_24h","o3_8h","o3_8h_24h" ,"so2" ,"so2_24h", "Real_AQI"]
		self.csv=pd.read_csv(filePath,names=names,parse_dates=True,index_col=0,header=0)
