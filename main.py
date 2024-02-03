import requests
import pygame as pg
import help
from pprint import pprint


geocoder_params = {"apikey": help.GEOCODER_APIKEY, "geocode": help.START_PLACE, "format": "json"}
resp = requests.get(help.GEOCODER_SERVER, params=geocoder_params)
js = resp.json()
geo_obj = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
start_coords = ",".join(geo_obj["Point"]["pos"].split())
#pprint(js)
#pprint(geo_obj)
static_params = {"ll": start_coords, "l": "sat", "spn": "1,1"}
resp = requests.get(help.STATIC_MAPS_SERVER, params=static_params)
with open("mp.png", "wb") as mp:
    mp.write(resp.content)
pg.init()
mp = pg.image.load("mp.png")
SCREEN = pg.display.set_mode(mp.get_size())
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            break
        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_ESCAPE]:
                pg.quit()
                break
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(mp, (0, 0))
    pg.display.flip()