from mobiletrans.mtdistmap.dijkstra.dijkstra import shortestPath
from UserDict import DictMixin
from pprint import pprint

class Station(DictMixin):
    def __init__(self, line, name, links, *args, **kwargs):
        self.line = line
        self.name = name
        self.links = links
        self.desc = kwargs.get('desc', "")
    def __getitem__(self, key):
        return self.links[key]
    def __setitem__(self, key, item):
        self.links[key] = item
    def __delitem__(self, key):
        del self.links[key]
    def keys(self):
        return self.links.keys()
    def __repr__(self):
        return 'Station(line=%s name=%s desc=%s)' % (self.line, self.name, self.desc)
    def get_unique_name(self):
        return "%s_%s" % (self.line, self.name)

class Path(object):
    def __init__(self, tn, stops, total_time):
        self.tn = tn
        self.stops = stops
        self.total_time = total_time
    def as_stations(self):
        return [ self.tn[stop]  if tn.haskey(stop) else "walk"  for stop in self.stops ]
    def __repr__(self):
        return "Path(stops=%s total_time=%s)" % (self.stops, self.total_time)
    def pprint(self):
        return pprint(self.as_stations())

class TransitNetwork(DictMixin):
    def __init__(self, *args, **kwargs):
        """
        The constructor resets the station dictionary and the station path cache.
        """
        self.station_dict = {}
        self._path_cache = {} 
    def disjoin(self, key):
        """
        Function for splitting a transit stop key string into the appropriate parts. 
        This converts "Red_40560" into 'line=Red' and 'name=40560'
        """
        line, name = key.split("_")
        return (line, name)
    def rejoin(self, line, name):
        """
        This takes a transit line and a station name (id) and converts it
        to the keystring that the TransitNetwork object expects.
        """
        return "_".join([line,name])
    def __getitem__(self, key):
        """
        This overrides the Get property to make this TransitNetwork dictionary
        object store the line/stop info in a more rich data-structure.  
        Specifically, this stores the line/stop info into a 2-D dict, 
        where the first dimension is the transit line and the second 
        dimension is the stop name (id).
        """
        line, name = self.disjoin(key)
        return self.station_dict[line][name]
    def __setitem__(self, key, item):
        line, name = self.disjoin(key)
        self.station_dict[line] = {'name':item}
    def __delitem__(self, key):
        line, name = self.disjoin(key)
        del self.station_dict[line][name]
        if not len(self.station_dict[line]):
            del self.station_dict[line]
    def keys(self):
        keys = self.station_dict.keys()
        return keys
    def add_station(self, key, links, *args, **kwargs):
        """
        Adds a Station object to the network.  This takes
        a dictionary.  The key argument is the station
        key (i.e. <line>_<stop_id>) and the links argument
        is another dictionary containing key/value pairs 
        where the keys is the station key of a neighbor
        station, and the value is the time in minutes that
        it takes to travel to that station from the current
        station. 
        
        For example: 
        self.add_station('Red_41190', { 'Red_40100':1, 'Red_40900':2 }, desc='Jarvis Red')
        
        This method also takes an optional desc argument
        which adds a station description to the Station object.
        
        This method only creates a station going one way.  For example, 
        one may use this method to create a link between 
        station "Red_A" and "Red_B", but that does not imply a link
        from station "Red_B" to "Red_A".  That that connection
        must be made separately. 
        
        """
        root_cost = 0
        line, name = self.disjoin(key)
        station_start_key = self.rejoin("start", name)
        station_end_key = self.rejoin("end", name)
        
        links.update({station_end_key:root_cost})
        
        station = Station(line, name, links, *args, **kwargs)
        if not self.station_dict.has_key(line):
            self.station_dict[line] = {name:station}
        else:
            self.station_dict[line].update({name:station})
            
        if not self.has_key(station_start_key):
            station_start = Station("start", name, links={key:root_cost})
            if not self.station_dict.has_key("start"):
                self.station_dict["start"] = {name:station_start}
            else:
                self.station_dict["start"].update({name:station_start})
        else:
            self[station_start_key].links.update({key:root_cost})

        if not self.has_key(station_end_key):
            station_end = Station("end", name, links={})
            if not self.station_dict.has_key("end"):
                self.station_dict["end"] = {name:station_end}
            else:
                self.station_dict["end"].update({name:station_end})
            
    def get_stops_on_line(self, line):
        """
        This method takes a line identifier and returns
        all of the station keys (stations) on that line. 
        
        For example: 
            >>> tn.get_stops_on_line('P')
            ['P_40380', 'P_40640', 'P_40200', 'P_40850', 
             'P_40460', 'P_40260', 'P_40730', 'P_40040', 'P_40160', 'P_40680']
        """
        return_value = []
        if self.station_dict.has_key(line):
            return_value =  [self.rejoin(line, stop) for stop in self.station_dict[line].keys()]
        return return_value
    def get_stops_at_station(self, name):
        """
        Takes a station id and returns all of the stops at that station. 
        
        For example:
            >>> tn.get_stops_at_station('40260')
            ['Pink_40260', 'G_40260', 'P_40260', 'Brn_40260', 'Org_40260']
        """
        keys = []
        for line, v in self.station_dict.items():
            if v.has_key(name):
                keys.append(self.rejoin(line,name))
        return keys 
    def _shortest_path(self, start, end):
        return shortestPath(self, start, end)
    def shortest_path_raw(self, start, end, reverse=False):
        """
        This determines the shortest path between two 
        stops.  The start and end parameters must take
        valid station keys in the form of <line>_<stop_id>.
        For example, 
            shortest_path_raw('start_40560', 'end_40680')
        
        If the reverse parameter is set to True, 
        that effectively reverses the direction of the path.
        It will search from end to start instead.  
        
        The results of this method are cached in the 
        TransitNetwork object, for any given start/end pair
        passed in.  The path calculation will only take
        place the first time the start/end pair is provided.
        """
        if reverse:
            tmp=start
            start=end
            end=tmp
        cache_key = "%s.%s" % (start, end)
        if self._path_cache.has_key(cache_key):
            return_value = self._path_cache[cache_key]
        else:
            return_value = self._shortest_path(start, end)
            self._path_cache[cache_key] = return_value
        return Path(self, return_value[0], return_value[1])
    def shortest_path(self, start, end, reverse=False):
        """
        Pass in a stop id for the start and end stop.
        Get a shortest path back.
        For example:
            tn.shortest_path('40820', '41160')
        """
        if reverse:
            tmp = start
            start = end
            end = tmp
        start = self.rejoin('start', start)
        end = self.rejoin('end', end)
        return self.shortest_path_raw(start, end)
    def clear_path_cache(self):
        """
        This clears the path cache.  Only used if one needs
        to recalculate the cached start/end values for some
        reason. 
        """
        self.path_cache = {}
    def __repr__(self):
        return 'TransitNetwork(<>)'
