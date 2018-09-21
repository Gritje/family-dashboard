import json
import requests
from pprint import pprint

class YWeather():
    
    def __init__(self):
    
        self.temp = '?'
        self.high = '?'
        self.low = '?'
        self.weatherText = 'Sunny'
        self.picUrl = '?'
        
        self.textToPicUrlMap = {'' : 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/rain_day_night@2x.png',
            'Partly Cloudy' : 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/partly_cloudy_day@2x.png',
            'Mostly Cloudy' : 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/mostly_cloudy_day_night@2x.png',
            'Cloudy' : 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/cloudy_day_night@2x.png',
            'Sunny' : 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/clear_day@2x.png',
            'Fair' : 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/fair_day@2x.png',
            'Showers' : 'https://s.yimg.com/os/weather/1.0.1/shadow_icon/60x60/rain_day_night@2x.png'}
        
        self.fetchWeatherData()
        
    def fetchWeatherData(self):
        
        try:
        
            self.response = requests.get('https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22luebeck%22)%20and%20u%3D%22c%22&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys')
            #print(response.text)
            self.parsed_json = json.loads(self.response.text)
            self.temp = self.parsed_json["query"]["results"]["channel"]["item"]["condition"]["temp"]
            self.high = self.parsed_json["query"]["results"]["channel"]["item"]["forecast"][0]["high"]
            self.low = self.parsed_json["query"]["results"]["channel"]["item"]["forecast"][0]["low"]
            self.weatherText = self.parsed_json["query"]["results"]["channel"]["item"]["condition"]["text"]
            self.picUrl = self.textToPicUrlMap.get(self.weatherText)   

        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)          
