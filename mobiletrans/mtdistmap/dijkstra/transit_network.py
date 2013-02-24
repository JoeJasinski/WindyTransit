from mobiletrans.mtdistmap.dijkstra.dijkstra import shortestPath
from UserDict import DictMixin

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

class TransitNetwork(DictMixin):
    def disjoin(self, key):
        line, name = key.split("_")
        return (line, name)
    def rejoin(self, line, name):
        return "_".join([line,name])
    def __init__(self, *args, **kwargs):
        self.station_dict = {}
        self._path_cache = {}
    def __getitem__(self, key):
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
        line, name = self.disjoin(key)
        station = Station(line, name, links, *args, **kwargs)
        if not self.station_dict.has_key(line):
            self.station_dict[line] = {name:station}
        else:
            self.station_dict[line].update({name:station})
    def get_stops_on_line(self, line):
        return_value = []
        if self.station_dict.has_key(line):
            return_value =  [self.rejoin(line, stop) for stop in self.station_dict[line].keys()]
        return return_value
    def get_stops_at_station(self, name):
        keys = []
        for line, v in self.station_dict.items():
            if v.has_key(name):
                keys.append(self.rejoin(line,name))
        return keys 
    def _shortest_path(self, start, end):
        return shortestPath(self, start, end)
    def shortest_path(self, start, end):
        cache_key = "%s.%s" % (start, end)
        if self._path_cache.has_key(cache_key):
            return_value = self._path_cache[cache_key]
        else:
            return_value = self._shortest_path(start, end)
            self._path_cache[cache_key] = return_value
        return return_value
    def clear_path_cache(self):
        self.path_cache = {}
    def __repr__(self):
        return 'TransitNetwork(<>)'
