import requests
def getinfo(city, api_key):
    url="https://api.openweathermap.org/data/2.5/weather"
    param={"q": city,"appid": api_key,"units": "metric"}
    response = requests.get(url, params=param)
    data = response.json()
    if response.status_code != 200:
        return data
    return data["main"]["temp"]
def checkfile(city, season,temp, stats):
    info=stats[(stats["city"] == city) & (stats["season"] == season)]
    if info.empty:
        return "Ошибка попробуйте еще раз"
    mean=info["mean"].values[0]
    std=info["std"].values[0]
    if temp>mean+2*std or temp<mean-2*std:
        return "Аномалия в показателях температуры"
    else:
        return "Температура находитсЯ в пределах нормы"
