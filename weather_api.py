import requests
from datetime import datetime

# Словарь перевода значений направления ветра
DIRECTION_TRANSFORM = {
    'n': 'северное',
    'nne': 'северо - северо - восточное',
    'ne': 'северо - восточное',
    'ene': 'восточно - северо - восточное',
    'e': 'восточное',
    'ese': 'восточно - юго - восточное',
    'se': 'юго - восточное',
    'sse': 'юго - юго - восточное',
    's': 'южное',
    'ssw': 'юго - юго - западное',
    'sw': 'юго - западное',
    'wsw': 'западно - юго - западное',
    'w': 'западное',
    'wnw': 'западно - северо - западное',
    'nw': 'северо - западное',
    'nnw': 'северо - северо - западное',
    'c': 'штиль',
}
def current_weather_api(city):
    token = '5d591e2cb44a4539b59115302231112'
    url = f'https://api.weatherapi.com/v1/current.json?key={token}&q={city}'
    response = requests.get(url)
    print(response.text)
    data = response.json()
    s = {'Город': data["location"]["name"],
        'Страна': data["location"]["country"],
        'Температура': data["current"]["temp_c"],
        'Ветер': data["current"]["wind_kph"],
        'Ощущается': data["current"]["feelslike_c"],
        'Время обновления': data["current"]["last_updated"]}
    return s

def current_weather(lat, lon):
    """
    Описание функции, входных и выходных переменных
    """
    token = 'fc49970d-6550-464c-b92b-ebe80078b1d3'  # Вставить ваш токен
    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"  # Если вдруг используете тариф «Погода на вашем сайте»
    # то вместо forecast используйте informers. url = f"https://api.weather.yandex.ru/v2/informers?lat={lat}&lon={lon}"
    headers = {"X-Yandex-API-Key": f"{token}"}
    response = requests.get(url, headers=headers)
    data = response.json()
    # print(response.json())

    # Данная реализация приведена для тарифа «Тестовый», если у вас Тариф «Погода на вашем сайте», то закомментируйте пару строк указанных ниже
    result = f'city: {data["info"]["tzinfo"]["name"]}\n'\
             f'time: {datetime.fromtimestamp(data["fact"]["uptime"]).strftime("%H:%M")}\n'\
             f'temp: {data["fact"]["temp"]}\n'\
             f'feels_like_temp: {data["fact"]["feels_like"]}\n'\
             f'pressure: {data["fact"]["pressure_mm"]}\n'\
             f'humidity: {data["fact"]["humidity"]}\n'\
             f'wind_speed: {data["fact"]["wind_speed"]}\n'\
             f'wind_gust: {data["fact"]["wind_gust"]}\n'\
             #f'wind_dir: DIRECTION_TRANSFORM.get(data['fact']['wind_dir']),  # Если используете Тариф «Погода на вашем сайте», то закомментируйте эту строку

    return result


if __name__ == "__main__":
    ...
    # print(current_weather(59.93, 30.31))  # Проверка работы для координат Санкт-Петербурга
    current_weather_api('Moscow')