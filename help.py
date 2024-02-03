GEOCODER_APIKEY = "40d1649f-0493-4b70-98ba-98533de7710b"
GEOSEARCH_APIKEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
START_PLACE = "город Самара"
GEOCODER_SERVER = "https://geocode-maps.yandex.ru/1.x"
GEOSEARCH_SERVER = "https://search-maps.yandex.ru/v1"
STATIC_MAPS_SERVER = "https://static-maps.yandex.ru/1.x"


def get_spn(response):
    bounds = response["properties"]["ResponseMetaData"]["SearchRequest"]["boundedBy"]
    spn = f"{abs(bounds[0][0] - bounds[1][0])},{abs(bounds[0][1] - bounds[1][1])}"
    return spn
