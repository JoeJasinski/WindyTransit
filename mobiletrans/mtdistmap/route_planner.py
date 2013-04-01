from __future__ import division
from django.contrib.gis.geos import Point, fromstr
from mobiletrans.mtlocation import models
from mobiletrans.mtdistmap.cta_conn import load_transitnetwork
from copy import deepcopy

def distance_to_time(distance, unit="m", units_per_min="60"):
    return getattr(distance, unit)  *  (1 / units_per_min ) 

class RoutePlanner(object):
    def __init__(self, tn, unit="m", units_per_min="60", max_distance=1500, num_routes=2):
        self.tn = tn
        self.unit = unit
        self.units_per_min = units_per_min
        self.max_distance = max_distance
        self.num_routes = num_routes
    def get_distance_dict(self):
        return {self.unit:self.max_distance}
    def fastest_route_from_point(self, point, station_id):
        distance_dict=self.get_distance_dict()
        stations = models.TransitStop.objects.filter(location_type=1).get_closest_x(point, distance_dict, number=self.num_routes ) 
        paths = []
        for station in stations: 
            path = self.tn.shortest_path(str(station.stop_id), station_id)
            if path:
                path_copy = deepcopy(path)
                walking_distance = station.distance
                walking_time = distance_to_time(walking_distance, self.unit, self.max_distance)
                path_copy.stops.insert(0, "walk_%s" % (walking_time))
                path_copy.total_time += walking_time 
                paths.append(path_copy)
        sorted(paths, key=lambda x:x.total_time)
        return paths         

"""
from mobiletrans.mtdistmap.cta_conn import load_transitnetwork
from mobiletrans.mtdistmap.route_planner import RoutePlanner
from django.contrib.gis.geos import Point, fromstr
from_point = fromstr('POINT(%s %s)' % ("-87.66638826", "41.96182144"))
#from_point = GPlace.objects.get(name__icontains='Precious Blood Church')
tn = load_transitnetwork()
t = RoutePlanner(tn)
p = t.fastest_route_from_point(from_point, '41320')
"""