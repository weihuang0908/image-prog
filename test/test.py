import sys
sys.path.append(".")
sys.path.append("../")
from core.service.aqidata import AqiData
from lib.pm25inClient import PM25inClient
from lib.mongoClient import MongoClient
from core.api.imageAnaly import ImageAnaly
imageAnaly=ImageAnaly()
pm25inClient =PM25inClient.PM25inClient()
aqi=AqiData()
currentDir="/Users/weihuang/Projects/image-prog/res/images/output/tResearch"
class TestCase(object):
	"""docstring for TestCase"""
	def __init__(self):
		super(TestCase, self).__init__()
	""" test spider of pm2.5 api"""
	def test(self):
		filepath=currentDir+"/P1150651_t3.JPG"
		imageAnaly.histEqual(filepath)

if __name__ == '__main__':
	test=TestCase()
	test.test()