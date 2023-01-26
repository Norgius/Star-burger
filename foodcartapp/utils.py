import requests
from geopy.distance import distance
from django.conf import settings


def fetch_coordinates(address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": settings.YANDEX_GEOCODER_APIKEY,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.\
        json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        raise requests.RequestException

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def calculate_distance(*address):
    try:
        address_one = fetch_coordinates(address[0])
        address_two = fetch_coordinates(address[1])
    except requests.RequestException:
        return None
    distance_between = distance(address_one, address_two).km
    return distance_between
