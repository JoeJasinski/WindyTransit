from dijkstra import shortestPath
from UserDict import DictMixin

class Station(DictMixin):
    def __init__(self, line, name, links):
        self.line = line
        self.name = name
        self.links = links
    def __getitem__(self, key):
        return self.links[key]
    def __setitem__(self, key, item):
        self.links[key] = item
    def __delitem__(self, key):
        del self.links[key]
    def keys(self):
        return self.links.keys()
    def __repr__(self):
        return 'Station(line=%s name=%s)' % (self.line, self.name,)
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
    def add_station(self, key, links):
        line, name = self.disjoin(key)
        station = Station(line, name, links)
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
    def shortest_path(self, start, end):
        return shortestPath(self, start, end)
    def __repr__(self):
        return 'TransitNetwork(<>)'


tn = TransitNetwork() 
tn.add_station('red_b', {'red_d':5}) 
tn.add_station('red_d', {'red_g':1, 'green_d':5, 'brown_d':5}) 
tn.add_station('red_g', {'red_d':1, 'red_i':1}) 
tn.add_station('red_i', {'red_k':1, 'blue_i':5}) 
tn.add_station('red_k', {'red_i':1, 'red_l':3, 'brown_k':5, }) 
tn.add_station('red_l', {'red_k':3}) 

tn.add_station('green_c', {'green_e':2})
tn.add_station('green_e', {'green_c':2, 'green_d':1, 'brown_e':5, 'blue_e':5})
tn.add_station('green_d', {'green_e':1, 'red_d':5, 'brown_d':5, 'green_h':3})
tn.add_station('green_h', {'green_d':3, 'green_j':2, 'brown_h':5})
tn.add_station('green_j', {'green_h':2, 'green_m':5, 'brown_j':5})
tn.add_station('green_m', {'green_j':5})

tn.add_station('blue_n', {'blue_e':2})
tn.add_station('blue_e', {'blue_n':2, 'blue_i':2, 'green_e':5, 'brown_e':5})
tn.add_station('blue_i', {'blue_e':2, 'blue_o':5, 'red_i':5})
tn.add_station('blue_o', {'blue_i':5})

tn.add_station('brown_a', {'brown_f':2})
tn.add_station('brown_f', {'brown_k':3})
tn.add_station('brown_k', {'brown_j':2, 'red_k':5})
tn.add_station('brown_j', {'brown_h':2, 'green_j':5})
tn.add_station('brown_h', {'brown_d':3, 'green_h':5})
tn.add_station('brown_d', {'brown_e':1, 'red_d':5, 'green_d':5})
tn.add_station('brown_e', {'brown_a':2, 'blue_e':5, 'green_e':5})



tn.shortest_path('green_c', 'red_k')
tn.get_stops_on_line('green')
tn.get_stops_at_station('e')




