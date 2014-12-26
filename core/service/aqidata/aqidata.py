import json
import codecs
import requests
# from bs4 import UnicodeDammit
from BeautifulSoup import UnicodeDammit
from core.config import BaseConfig
from lib.mongoClient import MongoClient
from lib.pm25inClient import PM25inClient
from lib.pandaClient import PandaClient
"""
    PM2.5AQITable   calucator    
    0 - 50  0.0 - 15.0  0.0 – 12.0
    51 - 100    >15.0 - 40  12.1 – 35.4
    101 – 150   >40 – 65    35.5 – 55.4
    151 – 200   > 65 – 150  55.5 – 150.4
    201 – 300   > 150 – 250 150.5 – 250.4
    301 – 400   > 250 – 350 250.5 – 350.4
    401 – 500   > 350 – 500 350.5 – 500
"""
def pm25_to_aqi(x):
    if x<15:
        return x*3.3
    elif x<65:
        return 2*x+20
    elif x<150:
        return 150+(x-65)*0.58
    elif x<350:
        return x+50
    else:
        return 400+(x-350)*0.66

def aqi_to_pm25(x):
    if x<50:
        return x*0.3
    elif x<150:
        return 0.5*x-10
    elif x<200:
        return 65+(x-150)*1.72
    elif x<400:
        return x-50
    else:
        return 350+(x-400)*1.5

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
