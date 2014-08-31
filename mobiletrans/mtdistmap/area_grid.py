import logging, json
from Queue import Queue
from threading import Thread, Semaphore
from UserDict import DictMixin

#from mobiletrans.mtdistmap.utils import shapefile
import shapefile

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
    def generate_shapefile(self, shape_file_name='shapefiles/test'):
        """
        Exports the data grid into a set of shapefiles.  
        
        Input: 
        shape_file_name="/home/test/shapefiles/myshape"
        
        Output: 
        In directory /home/test/shapefiles/
           myshape.shp
           myshape.shx
           myshape.dbf
        
        """
        w = shapefile.Writer(shapeType=shapefile.POINT) 
        w.autoBalance = 1
        w.field('ID', 'N')  # id field of type Number
        w.field('x' , "N")
        w.field('y', "N")
        
        count = 1
        for i in self.items():
           graphpoint = i[1]
           w.point(graphpoint.point.x, graphpoint.point.y)
           w.record(count, graphpoint.x, graphpoint.y, )
           count += 1
        
        w.save(shape_file_name)


class GridGenerator(object):
    """
    Generate a grid of evenly spaced points across the region 
    area geography object.
  
    Executing the run() method will actually start the calculation.
    It will create generated a grid by first taking a start 
    point and then visit points to the north, south, east, and
    west of that point.  This will continue until all points
    in the region have been visited. 

    Inputs:
    region - (required) the bounding region for the grid
    grid - (required) the empty new Grid object  
    """
    grid = None
    directions = ['north', 'south', 'east', 'west']
    num_worker_threads=4
    
    def __init__(self, region, grid, *args, **kwargs):
        self.q = Queue()
        self.region = region
        self.grid = grid

    @property
    def grid_point_class(self):
        return GridPoint

    def transpose(self, grid_point, azimuth, distance):
        return g.fwd(grid_point.point.x, grid_point.point.y, azimuth, distance)
  
    def north(self, grid_point):
        lng, lat, az =  self.transpose(grid_point, 0, self.grid.yint)
        return self.grid_point_class(grid_point.x, grid_point.y + self.grid.yint, Point(lng, lat))
    
    def south(self, grid_point):
        lng, lat, az =  self.transpose(grid_point, 180, self.grid.yint)
        return self.grid_point_class(grid_point.x, grid_point.y - self.grid.yint, Point(lng, lat), )
    
    def east(self, grid_point): 
        lng, lat, az = self.transpose(grid_point, 90, self.grid.xint)
        return self.grid_point_class(grid_point.x + self.grid.xint, grid_point.y, Point(lng, lat), )
    
    def west(self, grid_point): 
        lng, lat, az = self.transpose(grid_point, 270, self.grid.xint)
        return self.grid_point_class(grid_point.x - self.grid.xint, grid_point.y, Point(lng, lat),)

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
    """
    Generate a grid a cross the region area geography object 
    and calculate the routes to the given train stop (to_point) for each
    grid point.  
    Inputs:
    region - (required) the bounding region for the grid
    grid - (required) the empty new RouteGrid object
    to_point - (required) train stop id where all the grid point should search to
    max_distance - (default 1500) the max search radius around each search point in which
      to search for a nearby start train stop.
    num_routes - (default 2) will perform a route calculation for the closest num_routes
      to a given grid point.   
    
    """
    def __init__(self, to_point, *args, **kwargs):
        self.to_point = to_point
        tn = load_transitnetwork()
        self.t = RoutePlanner(tn, max_distance=kwargs.get('max_distance', 1500), 
                              num_routes=kwargs.get('num_routes', 2))
        super(RouteGridGenerator, self).__init__(*args, **kwargs)

    @property
    def grid_point_class(self):
        return RouteGridPoint
   
    def work(self, new_point):
        from_point = new_point.point
        p = self.t.fastest_route_from_point(from_point, self.to_point)
        new_point.routes += p



class RouteGrid(Grid):
    
    def generate_shapefile(self, shape_file_name='shapefiles/test'):
        """
        Exports the data grid into a set of shapefiles.  
        
        Input: 
        shape_file_name="/home/test/shapefiles/myshape"
        
        Output: 
        In directory /home/test/shapefiles/
           myshape.shp
           myshape.shx
           myshape.dbf
        
        """
        w = shapefile.Writer(shapeType=shapefile.POINT) 
        w.autoBalance = 1
        w.field('ID', 'N')  # id field of type Number
        w.field('NUM_ROUTES', 'N')  # route field of type Number
        w.field('x' , "N")
        w.field('y', "N")
        w.field('total_time', 'N', decimal=4) # long
        
        count = 1
        for i in self.items():
           graphpoint = i[1]
           w.point(graphpoint.point.x, graphpoint.point.y)
           w.record(count, len(graphpoint.routes), graphpoint.x, graphpoint.y, "%s" % graphpoint.shortest_time() )
           count += 1
        
        w.save(shape_file_name)


class RouteGridPoint(GridPoint):
    
    def __init__(self, *args, **kwargs):
        super(RouteGridPoint, self).__init__(*args, **kwargs)
        self.routes = []

    def __repr__(self):
        return "Route" + super(RouteGridPoint, self).__repr__()

    def shortest_route(self):
        return_value = None
        if self.routes:
            return_value = sorted( self.routes, key=lambda x: x.total_time,reverse=True)[0]
        return return_value

    def shortest_time(self, default=9999999):
        return_value = default
        route = self.shortest_route()
        if route:
            return_value = route.total_time
        return return_value
     
"""

# generate the grid with routes 
from mobiletrans.mtlocation.models import CityBorder
from mobiletrans.mtdistmap.area_grid import RouteGridGenerator, RouteGridPoint, RouteGrid
region = CityBorder.objects.all()[0]
center = region.area.centroid
grid = RouteGrid(xint=300, yint=300)
#gridgen = RouteGridGenerator('41320', region, grid, max_distance=2000, num_routes=3)
gridgen = RouteGridGenerator('40170', region, grid, max_distance=2000, num_routes=3)
g = gridgen.run(RouteGridPoint(0,0,center))
g.generate_shapefile('shapefiles/chicago_pts5')


"""
