import requests
import pygame as pg
import help
from pprint import pprint


def refresh_map():
    global current_zoom, mp
    check_zoom()
    static_params = {"ll": start_coords, "l": "map", "z": str(current_zoom)}  # "spn": ",".join(str(i) for i in current_spn)}
    resp = requests.get(help.STATIC_MAPS_SERVER, params=static_params)
    with open("mp.png", "wb") as mp:
        mp.write(resp.content)
    mp = pg.image.load("mp.png")


def check_zoom():
    global current_zoom
    if current_zoom > help.MAX_ZOOM or current_zoom > help.MAX_ZOOM:
        current_zoom = help.MAX_ZOOM
    elif current_zoom < help.MIN_ZOOM or current_zoom < help.MIN_ZOOM:
        current_zoom = help.MIN_ZOOM

geocoder_params = {"apikey": help.GEOCODER_APIKEY, "geocode": help.START_PLACE, "format": "json"}
resp = requests.get(help.GEOCODER_SERVER, params=geocoder_params)
js = resp.json()
geo_obj = js["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
start_coords = ",".join(geo_obj["Point"]["pos"].split())
#pprint(js)
#pprint(geo_obj)
print("Press UP ARROW to zoom out or DOWN ARROW to zoom in")
current_zoom = 2
refresh_map()
pg.init()
SCREEN = pg.display.set_mode(mp.get_size())
clock = pg.time.Clock()
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
            if keys[pg.K_UP]:
                current_zoom -= 1
                refresh_map()
            if keys[pg.K_DOWN]:
                current_zoom += 1
                refresh_map()
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(mp, (0, 0))
    pg.display.flip()
    #clock.tick(60)