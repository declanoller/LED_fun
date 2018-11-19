import pyowm




API_key = '04ffc6e961d525b4946f84b5c5b4008d'


owm = pyowm.OWM(API_key)


obs = owm.weather_at_place('boston, US')


w = obs.get_weather()


print(w.get_wind())




















#
