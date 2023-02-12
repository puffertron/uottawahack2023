import overpy
from pygame import Vector2
import pygame
import numpy as np
import math
import sys

class Road:
    def __init__(self:Vector2,start:Vector2, end, segments: list[tuple[Vector2,Vector2]]) -> None:
        self.length = 0
        self.segments = segments
        self.start_connections:list[Road] = []
        self.end_connections:list[Road] = []
        self.nodes = []
        self.start = start
        self.end = end
    
    def get_length(self): #TODO - make it so it does this once and never does it again
        length = 0
        for s in self.segments:
            dist = s[0].distance_to(s[1])
            length+= dist

        return length
    

class StreetMap:
    def __init__(self) -> None:
        self.streets = []
        self.originbbox = (45.386866,-75.660574, 45.379612,-75.675371)
        self.surf = None
        self.roads = []
    
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
    
    def map_coords_to_pixels(self) -> list[list[Vector2]]:
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

    def _draw_city_lines(self, roads):
        self.surf = pygame.Surface(pygame.display.get_window_size())
        width, height = self.surf.get_size()
        for way in roads:
            lastpoint = Vector2(way[0].x*width, way[0].y*height)
            for p in way:
                pxpoint = Vector2(width*p.x, height*p.y)
                pygame.draw.line(self.surf,"yellow", lastpoint, pxpoint,3)
                lastpoint = pxpoint

        return self.surf
    
    def draw_city_lines(self, roads: Road):
        self.surf = pygame.Surface(pygame.display.get_window_size())
        width, height = self.surf.get_size()
        x = 0
        for road in roads:
            x += 1
            colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "cyan", "magenta", "brown", "grey", "white"]
            for line in road.segments:    
                pxpoint1 = Vector2(width*line[0].x, height*line[0].y)
                pxpoint2 = Vector2(width*line[1].x, height*line[1].y)
                pygame.draw.line(self.surf,colors[x % len(colors)], pxpoint1, pxpoint2,3)

        return self.surf
    
    def initialise_road_segments(self) -> tuple[ list[tuple[Vector2,Vector2]], list[tuple[float, float]]]:
        roads = self.map_coords_to_pixels()
        
        segments = []
        xvalues = []
        for road in roads: 
            lastnode = road[0]
            count = 0
            for node in road:
                count += 1
                #create segments
                lastx = lastnode.x
                x = node.x
                segment = (lastnode, node)
                xpair = [lastx, x]
                segments.append(segment)
                xvalues.append(xpair)
                lastnode = node

        return segments, xvalues

    def index(l, f):
        return next((i for i in xrange(len(l)) if f(l[i])), None)

    def merge_segments(self, segments: list[tuple[Vector2,Vector2]], xvalues: list[list[float, float]]):
        z = zip(segments, xvalues)

        roads = []
        for i, seg in enumerate(z):
            seggroup = []
            #x coord
            #x1 = xvalues.pop(i)[0]
            x1 = xvalues[i][0]
            x2 = xvalues[i][1]
            #query
            qu = np.array(xvalues, dtype=object)
            indicies1 = np.where(qu == x1)[0]
            indicies2 = np.where(qu == x2)[0]

            indicies = indicies1.tolist() + indicies2.tolist()

            for i in indicies:
                select = segments[i]
                seggroup.append(select)
                
            start = seg[0]
            end = seggroup[-1]
            r = Road(start, end, seggroup)

            roads.append(r)

        return roads

            
    def populate_linked_list_network(roads: list[Road]):
        for road in roads: #TODO - make it so it populates both sides at once to make way more efficient
            #Do this process twice, once for start points, once for end points
            StreetMap.populate_road_ll(road, roads, True)
            StreetMap.populate_road_ll(road, roads, False)
            
            
    #function only used in populate_linked_list_network
    def populate_road_ll(source_road:Road, roads:list[Road], is_start:bool): #TODO - make it not be taking the bool, theres a better way but rushed
        #If is_start is true, does at start points, if false, then end point
        source_coord = Vector2(0,0)
        populating_roads = []

        if is_start == True:
            source_coord = source_road.start
        else:
            source_coord = source_road.end

        #TODO - makle one func that does this since code in multiple places
        #z = zip(roads, xvalues)

        for i, road in enumerate(roads):
            #x coord
            #x1 = xvalues.pop(i)[0]
            x1 = road.start.x
            x2 = road.end.x
            #query
            
            #THIS IS OLD CODE TO DELETE
                # qu = np.array(xvalues, dtype=object)
                # indicies1 = np.where(qu == x1)[0]
                # indicies2 = np.where(qu == x2)[0]

                # indicies = indicies1.tolist() + indicies2.tolist()

                # for i in indicies:
                #     select = segments[i]
                #     seggroup.append(select)
                    
                # start = seg[0]
                # end = seggroup[-1]
                # r = Road(start, end, seggroup)

                # roads.append(r)
        #Find roads with same x pos (either start or end)
        #Check that they have same y pos



        #Populate links (only for source)
        if is_start == True:
            source_road.start_connections = populating_roads
        else:
            source_road.end_connections = populating_roads
        
    
                
        
        
        
      ####### ATTEMPT 2  
        
        # #check all first nodes
        # road = []

        # segx = []
        # segx2 = []
        # for s in segments:
        #     segx.append(s[0])
        #     segx2.append(s[1])

        # for segment in segments:
        #     tx = segments.pop(0)
        #     if tx in segx:
        #         c = segx.count(segx[0])
        #         i = segx.index(tx)
        #         #join into road 
        #         if c == 1:
        #             conn = segments[i]
        #             road.append(conn[3],conn[4])
        #             print(conn)




###### ATTEMPT 1

        # # segmentssorted = segments.sort()
        # segments = list(segments)
        # segx = []
        # segx2 = []
        # for z in segments:
        #     zl = list(z)
        #     x1 = zl.pop(0)
        #     #x2 = zl.pop(1)
        #     if x1[0] in zl
            

        # # for i, seg in enumerate(segments):
        # #     #chck all first points, find matches
        # #     tx = segx.pop(i)
        # #     if tx in segx:
                



# m = StreetMap()

# s,x = m.initialise_road_segments()
# m.merge_segments(s,x)







    # def initialise_road_segments(self):
    #     roads = self.map_coords_to_pixels()
        
    #     extremes = []
    #     #confusing as heck, 'road' is a list of nodes, roads is a list of lists of nodes
    #     for road in roads:
    #         extremes.append(road[0]) #add the first point of each road to the list of extremes
    #         extremes.append(road[-1]) #add the last point of each road to the list of extremes

    #         segments = []
    #         length = 0
    #         lastnode = road[0]
    #         for node in road:
    #             dist = lastnode.distance_to(node)

    #             #create segments
    #             if lastnode != node:
    #                 segment = (lastnode, node)
    #                 segments.append[segment]
                
    #             length +=dist
    #             lastnode = node
            
        
    #         r = Road(length, road, segments)
    #         self.roads.append(r)

            
        


    
    
