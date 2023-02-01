import sys

import requests
from location.models import Location
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
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lat, lon


def get_or_create_coordinates(address, locations):
    try:
        for location in locations:
            if address == location.address:
                lat, lon = location.lat, location.lon
                return lat, lon
        coords = fetch_coordinates(address)

        if not coords:
            lat, lon = None, None
        else:
            lat, lon = coords
        Location.objects.create(
            address=address,
            lat=lat,
            lon=lon
        )
        return lat, lon
    except requests.RequestException as request_excepion:
        sys.stderr.write(f'Сетевая ошибка геокодера - {request_excepion}\n')
        return None, None
