import logging, json
from Queue import Queue
from threading import Thread
from UserDict import DictMixin

from django.contrib.gis.geos import Point
from pyproj import Geod

logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

g = Geod(ellps='WGS84')

class GridPoint(object):
    """
    This represents a geographic coordinate and
    where it falls on the Grid object.  The value
    of x and y refer to the x or y distance from the
    origin.  The xint and yint are the spacings between
    points.  
    """
    def __init__(self, x, y, point,):
        self.x = x
        self.y = y
        self.point = point
    
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
    
        
"""
from mobiletrans.mtdistmap.area_grid import generate_grid, GridPoint 
region = CityBorder.objects.all()[0]
gp = GridPoint(0, 0, region.area.centroid)
g = generate_grid(region, gp)
"""

class Grid(DictMixin):
    """
    This represents a grid of GridPoints, the center of which
    is at (0,0).  The key to this dict-like object is an (x,y)
    tuple representing the distance from the origin (0,0).
    """
    def __init__(self, xint, yint, *args, **kwargs):
        self.grid = {}
        self.xint = xint
        self.yint = yint
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
    grid = None
    directions = ['north', 'south', 'east', 'west']
    num_worker_threads=4
    
    def __init__(self, region, grid, *args, **kwargs):
        self.q = Queue()
        self.region = region
        self.grid = grid

    def transpose(self, grid_point, azimuth, distance):
        return g.fwd(grid_point.point.x, grid_point.point.y, azimuth, distance)
  
    def north(self, grid_point):
        lng, lat, az =  self.transpose(grid_point, 0, self.grid.yint)
        return GridPoint(grid_point.x, grid_point.y + self.grid.yint, Point(lng, lat))
    
    def south(self, grid_point):
        lng, lat, az =  self.transpose(grid_point, 180, self.grid.yint)
        return GridPoint(grid_point.x, grid_point.y - self.grid.yint, Point(lng, lat), )
    
    def east(self, grid_point): 
        lng, lat, az = self.transpose(grid_point, 90, self.grid.xint)
        return GridPoint(grid_point.x + self.grid.xint, grid_point.y, Point(lng, lat), )
    
    def west(self, grid_point): 
        lng, lat, az = self.transpose(grid_point, 270, self.grid.xint)
        return GridPoint(grid_point.x - self.grid.xint, grid_point.y, Point(lng, lat),)

    def create_grid(self, grid_point):
        for direction in self.directions:
            new_point = getattr(self, direction)(grid_point)
            if not self.grid.has_key((new_point.x, new_point.y)):
                self.grid[(new_point.x, new_point.y)] = new_point
                if self.region.area.contains(new_point.point):
                    self.work(new_point)
                    self.q.put(new_point)

    def work(self, new_point):
        pass

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
#from mobiletrans.mtdistmap.area_grid import GridGenerator, GridPoint, Grid
region = CityBorder.objects.all()[0]
center = region.area.centroid
grid = Grid(xint=300, yint=300)
gridgen = GridGenerator(region, grid)
g = gridgen.run(GridPoint(0,0,center))
"""


from mobiletrans.mtdistmap.cta_conn import load_transitnetwork
from mobiletrans.mtdistmap.route_planner import RoutePlanner
from django.contrib.gis.geos import Point, fromstr

class RouteGridGenerator(GridGenerator):
    
    def __init__(self, to_point, *args, **kwargs):
        self.to_point = to_point
        tn = load_transitnetwork()
        self.t = RoutePlanner(tn)
        super(RouteGridGenerator, self).__init__(*args, **kwargs)
         
    def work(self, new_point):
        from_point = new_point.point
        p = self.t.fastest_route_from_point(from_point, self.to_point)
        new_point.routes = p


class RouteGridPoint(GridPoint):
    
    def __init__(self):
        self.routes = []
    
     
"""
from mobiletrans.mtdistmap.area_grid import RouteGridGenerator, GridPoint, Grid
region = CityBorder.objects.all()[0]
center = region.area.centroid
grid = Grid(xint=300, yint=300)
gridgen = RouteGridGenerator('41320', region, grid)
g = gridgen.run(RouteGridPoint(0,0,center))
"""
