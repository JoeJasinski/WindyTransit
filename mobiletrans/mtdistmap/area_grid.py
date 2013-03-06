import logging, json
from Queue import Queue
from threading import Thread
from UserDict import DictMixin

from django.contrib.gis.geos import Point
from pyproj import Geod


g = Geod(ellps='WGS84')

class GridPoint(object):
    def __init__(self, x, y, point, xint=300, yint=300):
        self.x = x
        self.y = y
        self.point = point
        self.xint = xint
        self.yint = yint 
    
    @property
    def grid_coords(self):
        return (self.x, self.y)
    
    @property
    def geo_coords(self):
        return self.point.x, self.point.y
    
    @property
    def geo_coords_r(self):
        return self.point.y, self.point.x
    
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
from mobiletrans.mtdistmap.area_grid import generate_grid, GridPoint 
region = CityBorder.objects.all()[0]
gp = GridPoint(0, 0, region.area.centroid)
g = generate_grid(region, gp)
"""

class Grid(DictMixin):
    def __init__(self, *args, **kwargs):
        self.grid = {}
    def __getitem__(self, key):
        return self.grid[key]
    def __setitem__(self, key, item):
        self.grid[key] = item
    def __delitem__(self, key):
        del self.grid[key]
    def keys(self):
        return self.grid.keys()
    def json(self):
        features = []
        for k, point in self.items():
            d = { "type": "Feature",
                   "geometry": {"type": "Point", "coordinates": point.geo_coords},
            }
            features.append(d)
              
        json_dict = { "type": "FeatureCollection",
          "features": features
         }
        return json.dumps(json_dict)

class GridGenerator(object):
    grid = Grid()
    directions = ['north', 'south', 'east', 'west']
    num_worker_threads=4
    
    def __init__(self, region):
        self.q = Queue()
        self.region = region
    
    def create_grid(self, grid_point):
        for direction in self.directions:
            new_point = getattr(grid_point, direction)
            if not self.grid.has_key((new_point.x, new_point.y)):
                self.grid[(new_point.x, new_point.y)] = new_point
                if self.region.area.contains(new_point.point):
                    logging.debug("New %s" % new_point)
                    self.q.put(new_point)

    def worker(self):
        while True:
            item = self.q.get()
            self.create_grid(item)
            self.q.task_done()
    
    def run(self, start_grid_point):
        for i in range(self.num_worker_threads):
             t = Thread(target=self.worker)
             t.daemon = True
             t.start()
        self.create_grid(start_grid_point)
        self.q.join()
        return self.grid


"""
from mobiletrans.mtdistmap.area_grid import GridGenerator, GridPoint
r = CityBorder.objects.all()[0]
gg = GridGenerator(r)
p = r.area.centroid
g = gg.run(GridPoint(0,0,p))
"""
