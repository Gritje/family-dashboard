import unittest

from yweather import YWeather

class TestYWeather(unittest.TestCase):

    def test_weather_json_parsing(self):
        weather = YWeather()
        weather.parseWeather("{\"product\":\"civillight\",\"init\":\"2020010500\",\"dataseries\":[{\"date\":20200105,\"weather\":\"cloudy\",\"temp2m\":{\"max\": 4,\"min\":-1 },\"wind10m_max\" : 3 }] }")
        self.assertEqual(weather.temp, '4')
        self.assertEqual(weather.high, '4')
        self.assertEqual(weather.low, '-1')
        self.assertEqual(weather.weatherText, 'cloudy')
        self.assertEqual(weather.picUrl, 'http://www.7timer.info/img/misc/about_two_cloudy.png')
        
if __name__ == '__main__':
    unittest.main()
    
