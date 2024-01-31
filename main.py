import sys
from io import BytesIO
import requests
from PIL import Image
import help

geosearch_api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
org_to_find = sys.argv[1:]

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "..."

address_ll = "37.588392,55.734036"

search_params = {
    "apikey": geosearch_api_key,
    "text": org_to_find,
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    pass

json_response = response.json()

organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]

point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
spn = help.get_spn(json_response)

map_params = {
    "ll": address_ll,
    "spn": spn,
    "l": "map",
    "pt": "{0},pm2dgl".format(org_point)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
with open("mp.png", "wb") as f:
    f.write(response.content)