import overpy
from pygame import Vector2
import pygame
import math
import sys
import random

pygame.init()
size = width, height = 320, 240
middle = Vector2(width/2, height/2)

# creating surfaces to draw on, background and dots layer
# (layer for truck is stored in truck class)
screen = pygame.display.set_mode(size)
streetmap = screen.copy()

def latlondist2m(lat1,lon1, lat2,lon2):
    latMid = (lat1+lat2)/2.0
    m_per_lat = 111132.954 - 559.822 * math.cos( 2.0 * latMid ) + 1.175 * math.cos( 4.0 * latMid)
    m_per_lon = (math.pi/180 ) * 6367449 * math.cos ( latMid )

    deltaLat = math.fabs(lat1-lat2)
    deltaLon = math.fabs(lon1-lon2)

    dist_m = math.sqrt(math.pow(deltaLat * m_per_lat, 2) + math.pow(deltaLon * m_per_lon, 2))

    return dist_m



originbbox = (45.386866,-75.660574, 45.379612,-75.675371) # 0=n, 1=e, 2=s, 3=w #TODO: ADD TO CONFIG

# (w,s) - (w,n), (w,s) - (s, e)
y = latlondist2m(originbbox[3], originbbox[2], originbbox[3], originbbox[0])
x = latlondist2m(originbbox[3], originbbox[2], originbbox[1], originbbox[2])
bboxmetres = Vector2(x,y)



print(bboxmetres)

api = overpy.Overpass()
result = api.query(f"""<osm-script>
 <query type="way">
  	<bbox-query n="45.386866" e="-75.660574" s="45.379612" w="-75.675371"/>
    <has-kv k="highway"/>
  	<has-kv k="footway|service|amenity|crossing" modv="not" regv="."/>
  	<has-kv k="bus" modv="not" regv="yes"/>
  	<has-kv k="highway" modv="not" regv="path|footway|steps|stop"/>
</query>
<union>
  <item/>
  <recurse type="down"/>
</union>
<print/>
</osm-script>""")



roads = []

for way in result.ways:
    coords = []
    for node in way.nodes:
        point = (float(node.lat),float(node.lon))
        #mpoint = latlondist2m(originbbox[0],originbbox[3],point[0],point[1])
        deltabbox = (originbbox[1]-originbbox[3], originbbox[0]-originbbox[2])
        deltapoint = (originbbox[1]-point[1], originbbox[0]-point[0])
        pointpercent = Vector2(deltapoint[0]/deltabbox[0], deltapoint[1]/deltabbox[1])
        coords.append(pointpercent)

    roads.append(coords)

# print(coords)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    for way in roads:
        lastpoint = Vector2(way[0].x*width, way[0].y*height)
        for p in way:
            pxpoint = Vector2(width*p.x, height*p.y)
            col = "yellow"
            pygame.draw.line(streetmap,col, lastpoint, pxpoint,3)
            lastpoint = pxpoint

    # lastpoint = Vector2(coords[0].x*width, coords[0].y*height)
    # for p in coords:
    #     pxpoint = Vector2(width*p.x, height*p.y)
    #     pygame.draw.circle(streetmap,"orange", pxpoint,2)
    

    screen.fill("black")
    screen.blit(streetmap, streetmap.get_rect(), special_flags=pygame.BLEND_ADD)
    pygame.display.flip()