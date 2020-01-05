import json
import requests

class YWeather():
    
    def __init__(self):
    
        self.temp = '?'
        self.high = '?'
        self.low = '?'
        self.weatherText = 'clear'
        self.picUrl = '?'
        
        self.textToPicUrlMap = {'' : 'http://www.7timer.info/img/misc/about_two_clear.png',
            'clear' : 'http://www.7timer.info/img/misc/about_two_clear.png',
            'mcloudy' : 'http://www.7timer.info/img/misc/about_two_pcloudy.png',
            'cloudy' : 'http://www.7timer.info/img/misc/about_two_cloudy.png',
            'rain' : 'http://www.7timer.info/img/misc/about_two_rain.png',
            'snow' : 'http://www.7timer.info/img/misc/about_two_snow.png',
            'ts' : 'http://www.7timer.info/img/misc/about_two_ts.png',
            'tsrain' : 'http://www.7timer.info/img/misc/about_two_tsrain.png'}
        
        self.fetchWeatherData()
        
    def fetchWeatherData(self):
        
        try:
        
            self.response = requests.get('http://www.7timer.info/bin/civillight.php?lon=10.7&lat=53.9&ac=0&unit=metric&output=json')
            
            if self.response.status_code == 200 :
                self.parseWeather(self.response.text)                  

        except Exception as e:
            print(type(e))
            print(e.args)
            print(e)          

    def parseWeather(self, weatherJson):
        self.parsed_json = json.loads(weatherJson)
        self.temp = str(self.parsed_json["dataseries"][0]["temp2m"]["max"])
        self.high = str(self.parsed_json["dataseries"][0]["temp2m"]["max"])
        self.low = str(self.parsed_json["dataseries"][0]["temp2m"]["min"])
        self.weatherText = self.parsed_json["dataseries"][0]["weather"]
        self.picUrl = self.textToPicUrlMap.get(self.weatherText)    
        