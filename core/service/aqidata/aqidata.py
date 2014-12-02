import json
import codecs
import requests
# from bs4 import UnicodeDammit
from BeautifulSoup import UnicodeDammit
from core.config import BaseConfig
from lib.mongoClient import MongoClient
from lib.pm25inClient import PM25inClient
from lib.pandaClient import PandaClient
mongo = MongoClient(BaseConfig.MONGO_ADDRESS, BaseConfig.MONGO_PORT, BaseConfig.MONGO_USER,
                    BaseConfig.MONGO_PASS)
pm25in=PM25inClient.PM25inClient()
panda=PandaClient()
class AqiData(object):
    def __init__(self):
        pass
    def daily_fetch_insert(self):
        data=pm25in.curl_city_pollutant()
        self.time_format(data)
        _id=mongo.insert_into_col_1(data)#insert
        print "insert"+ _id
    def history_fetch_insert(self):
        filepath=BaseConfig.HISTORY_CSV_PATH
        panda.read_csv(filepath)

    def mongoRes_to_json(self,data):
        res={}
        res["org"]=data["org"]
        res["count"]=string.atof(data["typeScore"][0]["count"])
        return res
    def time_format(self,data):
        for item in data:
            time_point=item["time_point"]
            time_point=time_point[:-1].replace('T',' ')
            item["time_point"]=time_point
