import logging
from Queue import Queue
from threading import Thread

from django.contrib.gis.geos import Point
from pyproj import Geod


g = Geod(ellps='WGS84')

class GridPoint(object):
    def __init__(self, x, y, point, xint=300, yint=300):
        self.xint = xint
        self.yint = yint
        self.point = point
        self.x = x
        self.y = y 
    
    @property
    def grid_coords(self):
        return (self.x, self.y)
    
    @property
    def geo_coords(self):
        return_value = (self.point.x, self.point.y)
    
    @property
    def geo_coords_r(self):
        return_value = (self.point.y, self.point.x)
    
    def __repr__(self):
        return "GridPoint(lng=%s (%s), lat=%s (%s))" % (
                self.point.x, self.x, self.point.y, self.y)
    
    def transpose(self, azimuth, distance):
        return g.fwd(self.point.x, self.point.y, azimuth, distance)
    
    @property
    def north(self):
        lng, lat, az =  self.transpose(0, self.yint)
        return GridPoint(self.x, self.y + self.yint, Point(lng, lat), self.xint, self.yint)
    
    @property
    def south(self):
        lng, lat, az =  self.transpose(180, self.yint)
        return GridPoint(self.x, self.y - self.yint, Point(lng, lat), self.xint, self.yint)
    
    @property
    def east(self): 
        lng, lat, az = self.transpose(90, self.xint)
        return GridPoint(self.x + self.xint, self.y, Point(lng, lat), self.xint, self.yint)
    
    @property
    def west(self): 
        lng, lat, az = self.transpose(270, self.xint)
        return GridPoint(self.x - self.xint, self.y, Point(lng, lat), self.xint, self.yint)
        
"""
region = CityBorder.objects.all()[0]
gp = GridPoint(0, 0, region.area.centroid)
g = generate_graph(region, gp)
"""

def generate_graph(region, gp):
    graph = {}
    directions = ['north', 'south', 'east', 'west']
        
    q = Queue()
    
    def create_grid(grid_point):
        for direction in directions:
            new_point = getattr(grid_point, direction)
            if not graph.has_key((new_point.x, new_point.y)):
                graph[(new_point.x, new_point.y)] = new_point
                if region.area.contains(new_point.point):
                    print "New", new_point 
                    q.put(new_point)
                else:
                    """ """
                    #print "Out of bounds", new_point
            else:
                """ """
                #print "Existing", new_point
    
    num_worker_threads=4
    
    def worker():
        while True:
            item = q.get()
            create_grid(item)
            q.task_done()
            
    for i in range(num_worker_threads):
         t = Thread(target=worker)
         t.daemon = True
         t.start()
    
    create_grid(gp)
    q.join()
    return graph

