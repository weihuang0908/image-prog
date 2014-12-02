# -*- coding: utf-8 -*-
import json
import codecs
from datetime import date
import requests
from BeautifulSoup import BeautifulSoup
class PM25inClient(object):
    def __init__(self):
        self.token='CmcUvqxZafMsKxLiaEoK'#appKey
        self.base_url="http://www.pm25.in/api/querys/"
        _today=date.today
    def curl_history_aqi(self,hour=14,year=2014,month=11,day=1,number=1,unit=1,cn=0):
        #number{1day,2day,...}
        #unit:{0:hour,1:day,2:week,3:year}
        #action:{0:hour graph,1:daily summary graph,2:data only}
        #cn:{0:us level,1:china level}
        url = "http://young-0.com/airquality/index.php"
        params = {
            "number": number,
            "unit": unit,
            "enddate":1,
            "year":year,
            "month":month,
            "day":day,
            "hour":hour,
            "city":0,
            "cn":cn,
            "action":2
        }
        try:
            response = requests.get(url, params=params)
            data=[]
            table=  BeautifulSoup(response.text).table
            if table.find('tbody') is None:
                rows=table.findAll('tr')
            else:
                rows = table_body.findAll('tr')
            for row in rows:
                dic={}
                cols = row.findAll('td')
                if len(cols)==4:
                    dic["time_point"]=cols[1].text.strip()
                    dic["pm2_5"]=int(cols[2].text.strip())
                    data.append(dic) # Get rid of empty values
            print data
        except:
            data = []
        return data
    def curl_pm2_5(self):
    	return self.curl_city_pollutant("pm2_5")
    def curl_pm10(self):
    	return self.curl_city_pollutant("pm10")
    def curl_co(self):
    	return self.curl_city_pollutant("co")
    def curl_no2(self):
    	return self.curl_city_pollutant("no2")
    def curl_so2(self):
    	return self.curl_city_pollutant("no2")
    def curl_o3(self):
    	return self.curl_city_pollutant("no2")    	
    def curl_city_pollutant(self,pollutant="aqi_details",city="beijing",isAllMoniPoint=True):
        #polutant=[pm2_5,pm10,co,no2,so2,03]
        url = self.base_url+pollutant+".json"
        params = {
            "city": city,
            "token": self.token
        }
        try:
            response = requests.get(url, params=params)
            result=json.loads(response.text)
        except:
            result = {}
        return result
   #  """
   #      #station_code=range[1001A,1012A]
		 # position_name" : "万寿西宫", "station_code" : "1001A" 
		 # position_name" : "定陵", "station_code" : "1002A" 
		 # position_name" : "东四", "station_code" : "1003A" 
		 # position_name" : "天坛", "station_code" : "1004A" 
		 # position_name" : "农展馆", "station_code" : "1005A" 
		 # position_name" : "官园", "station_code" : "1006A" 
		 # position_name" : "海淀区万柳", "station_code" : "1007A" 
		 # position_name" : "顺义新城", "station_code" : "1008A" 
		 # position_name" : "怀柔镇", "station_code" : "1009A" 
		 # position_name" : "昌平镇", "station_code" : "1010A" 
		 # position_name" : "奥体中心", "station_code" : "1011A" 
		 # position_name" : "古城", "station_code" : "1012A" 
   #  """
    def curl_station_pollutant(self,station_code="1011A",isAllMoniPoint=True):
        url = self.base_url+"aqis_by_station.json"
        params = {
            "city": city,
            "token": self.token
        }
        try:
            response = requests.get(url, params=params)
            result=json.loads(response.text)
        except:
            result = {}
        return result