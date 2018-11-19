from weather import Weather, Unit

loc = 'providence, RI'

weather = Weather(unit=Unit.FAHRENHEIT)
location = weather.lookup_by_location(loc)
condition = location.condition
print(condition.text)






def simplifyWeather(long_form):

    long_form = long_form.lower()
    long_form = long_form.replace('partly ','')
    long_form = long_form.replace('mostly ','')

    f = open('condition_list.txt', 'r')
    weather_dict = f.read()
    weather_dict = [' '.join(x.split()[1:]) for x in weather_dict.split('\n') if len(x)>0]
    weather_dict = [x.split(' (')[0] for x in weather_dict]
    weather_dict = dict(zip(list(range(len(weather_dict))), weather_dict))
    #print(weather_dict)
    weather_to_num = dict(zip(weather_dict.values(), weather_dict.keys()))

    simplify_dict = {
    'thunderstorms': [3,4,37,38,39,45,47],
    'drizzle':[8,9],
    'snow':[13,14,15,16,41,42,43,46,48],
    'fog':[20,21],
    'windy':[23,24],
    'cloudy':[26,27,28,29,30,44],
    'fair':[33,34],
    'hail':[17,35]
    }
    #print(weather_to_num)
    #print(long_form)
    #print(weather_dict.values())
    if long_form in weather_dict.values():
        weather_code = weather_to_num[long_form]
        
        for key, val in simplify_dict.items():

            if weather_code in val:
                return(key)

        return(long_form)

    else:
        return(long_form)


print(simplifyWeather('Cloudy'))

location = weather.lookup_by_location(loc)
forecasts = location.forecast
for forecast in forecasts:
    print('\ndate:', forecast.date)
    print('text:', simplifyWeather(forecast.text))
    #print('text:', (forecast.text))
    print('high:', forecast.high)
    print('low:', forecast.low)









#
