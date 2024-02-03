import requests
import pygame as pg
import help
from pprint import pprint


def refresh_map():
    global current_zoom, current_coords, mp
    check_zoom()
    static_params = {"ll": ",".join(str(i) for i in current_coords), "l": "sat,skl", "z": str(current_zoom)}  # "spn": ",".join(str(i) for i in current_spn)}
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
print("Press PLUS to zoom out or MINUS to zoom in")
print("Use ARROWS to travel around the map")
current_zoom = 2
current_coords = [float(i) for i in start_coords.split(",")]
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
            if keys[pg.K_KP_PLUS] or keys[pg.K_PLUS] or keys[pg.KSCAN_KP_PLUS]:
                current_zoom -= 1
                refresh_map()
            if keys[pg.K_KP_MINUS] or keys[pg.K_MINUS] or keys[pg.KSCAN_KP_MINUS]:
                current_zoom += 1
                refresh_map()
            if keys[pg.K_UP]:
                current_coords[1] += 45 / 2 ** current_zoom
                refresh_map()
            if keys[pg.K_DOWN]:
                current_coords[1] -= 45 / 2 ** current_zoom
                refresh_map()
            if keys[pg.K_LEFT]:
                current_coords[0] -= 90 / 2 ** current_zoom
                refresh_map()
            if keys[pg.K_RIGHT]:
                current_coords[0] += 90 / 2 ** current_zoom
                refresh_map()
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(mp, (0, 0))
    pg.display.flip()
    #clock.tick(60)