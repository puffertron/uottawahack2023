import math
from pygame import Vector2
import pygame


class StreetMap:
    def __init__(self) -> None:
        self.streets = []
        self.originbbox = (45.386866,-75.660574, 45.379612,-75.675371)
        self.surf = pygame.Surface(pygame.display.get_window_size())
    
    def parse_OSM_data(self):
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

        return result
    
    def map_coords_to_pixels(self):
        result = self.parse_OSM_data()

        roads = []

        for way in result.ways:
            coords = []
            for node in way.nodes:
                point = (float(node.lat),float(node.lon))
                #mpoint = latlondist2m(originbbox[0],originbbox[3],point[0],point[1])
                deltabbox = (self.originbbox[1]-self.originbbox[3], self.originbbox[0]-self.originbbox[2])
                deltapoint = (self.originbbox[1]-point[1], self.originbbox[0]-point[0])
                pointpercent = Vector2(deltapoint[0]/deltabbox[0], deltapoint[1]/deltabbox[1])
                coords.append(pointpercent)

            roads.append(coords)
        
        return roads

    def draw_city_lines(self, roads):
        for way in roads:
            lastpoint = Vector2(way[0].x*width, way[0].y*height)
            for p in way:
                pxpoint = Vector2(width*p.x, height*p.y)
                pygame.draw.line(streetmap,"yellow", lastpoint, pxpoint,3)
                lastpoint = pxpoint

        return 

