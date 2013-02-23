from dijkstra import shortestPath
from UserDict import DictMixin

class Station(DictMixin):
    def __init__(self, line, name, links, *args, **kwargs):
        self.line = line
        self.name = name
        self.links = links
        self.desc = kwargs.get('desc', None)
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



tn = TransitNetwork() 
wait_time = 5.0
# transfer time for blue line to library at Jackson
bluelib_wait_time = 10.0
# transfer time for red line to library at Jackson
redlib_wait_time = 10.0
# 
red_blue_jackson_wait_time = 10.0

#>>> trans(['Brn', 'P'], '40460', desc="Merchandise Mart")
tn.add_station('Brn_40460', {'P_40460':wait_time, 'Brn_40730':2}, desc='Merchandise Mart')  # done
tn.add_station('P_40460', {'Brn_40460':wait_time, }, desc='Merchandise Mart')   # done loop

#>>> trans(['Brn', 'P', 'Org', 'Pink'], '40730', desc="Washington/Wells")
tn.add_station('Brn_40730', {'Org_40730':wait_time, 'P_40730':wait_time, 'Pink_40730':wait_time, 'Brn_40040':1, }, desc='Washington/Wells') # done
tn.add_station('P_40730', {'Brn_40730':wait_time, 'Org_40730':wait_time, 'Pink_40730':wait_time, 'P_40460':2, }, desc='Washington/Wells')   # done
tn.add_station('Org_40730', {'Brn_40730':wait_time, 'P_40730':wait_time, 'Pink_40730':wait_time, 'Org_40380':3 }, desc='Washington/Wells')  # done
tn.add_station('Pink_40730', {'Brn_40730':wait_time, 'Org_40730':wait_time, 'P_40730':wait_time, 'Pink_41160':3}, desc='Washington/Wells')  # done clinton estimate

#>>> trans(['Brn', 'P', 'Org', 'Pink'], '40040', desc="Quincy")
tn.add_station('Brn_40040', {'Pink_40040':wait_time, 'P_40040':wait_time, 'Org_40040':wait_time, 'Brn_40160':1, }, desc='Quincy') # done
tn.add_station('P_40040', {'Brn_40040':wait_time, 'Pink_40040':wait_time, 'Org_40040':wait_time, 'P_40730':1, }, desc='Quincy', ) # done
tn.add_station('Org_40040', {'Brn_40040':wait_time, 'Pink_40040':wait_time, 'P_40040':wait_time, 'Org_40730':1, }, desc='Quincy') # done
tn.add_station('Pink_40040', {'Brn_40040':wait_time, 'P_40040':wait_time, 'Org_40040':wait_time, 'Pink_40730':1 }, desc='Quincy') # done

#>>> trans(['Brn', 'P', 'Org', 'Pink'], '40160', desc="LaSalle")
tn.add_station('Brn_40160', {'P_40160':wait_time, 'Pink_40160':wait_time, 'Org_40160':wait_time, 'Brn_40850':1, }, desc='LaSalle') # done
tn.add_station('P_40160', {'Pink_40160':wait_time, 'Brn_40160':wait_time, 'Org_40160':wait_time, 'P_40040':1, }, desc='LaSalle') # done
tn.add_station('Org_40160', {'P_40160':wait_time, 'Pink_40160':wait_time, 'Brn_40160':wait_time, 'Org_40040':1, }, desc='LaSalle') # done
tn.add_station('Pink_40160', {'P_40160':wait_time, 'Brn_40160':wait_time, 'Org_40160':wait_time, 'Pink_40040':1 }, desc='LaSalle') # done

#>>> trans(['Brn', 'P', 'Org', 'Pink'], '40850', desc="Library")
tn.add_station('Brn_40850', {'Pink_40850':wait_time, 'P_40850':wait_time, 'Org_40850':wait_time, 'Blue_40070':bluelib_wait_time, 'Red_40560':redlib_wait_time, 'Brn_40680':2, }, desc='Library') # done
tn.add_station('P_40850', {'Brn_40850':wait_time, 'Pink_40850':wait_time, 'Org_40850':wait_time, 'Blue_40070':bluelib_wait_time, 'Red_40560':redlib_wait_time, 'P_40160':1, }, desc='Library')  # done
tn.add_station('Org_40850', {'Brn_40850':wait_time, 'Pink_40850':wait_time, 'P_40850':wait_time, 'Blue_40070':bluelib_wait_time, 'Red_40560':redlib_wait_time, 'Org_40160':1, }, desc='Library')  # done
tn.add_station('Pink_40850', {'Brn_40850':wait_time, 'P_40850':wait_time, 'Org_40850':wait_time, 'Blue_40070':bluelib_wait_time, 'Red_40560':redlib_wait_time, 'Pink_40160':1, }, desc='Library') # done

#>>> trans(['Brn', 'P', 'Org', 'G', 'Pink'], '40680', desc="Adams/Wabash")
tn.add_station('Brn_40680', {'P_40680':wait_time, 'G_40680':wait_time, 'Org_40680':wait_time, 'Pink_40680':wait_time, 'Brn_40640':1, }, desc='Adams/Wabash') # done
tn.add_station('P_40680', {'Brn_40680':wait_time, 'G_40680':wait_time, 'Org_40680':wait_time, 'Pink_40680':wait_time, 'P_40850':2, }, desc='Adams/Wabash') # done
tn.add_station('Org_40680', {'Brn_40680':wait_time, 'P_40680':wait_time, 'G_40680':wait_time, 'Pink_40680':wait_time, 'Org_41400':4, }, desc='Adams/Wabash') # done
tn.add_station('G_40680', {'Brn_40680':wait_time, 'P_40680':wait_time, 'Org_40680':wait_time, 'Pink_40680':wait_time, 'G_41400':3, 'G_40640':1, }, desc='Adams/Wabash') # done
tn.add_station('Pink_40680', {'Brn_40680':wait_time, 'P_40680':wait_time, 'G_40680':wait_time, 'Org_40680':wait_time, 'Pink_40850':2, }, desc='Adams/Wabash') # done

#>>> trans(['Brn', 'P', 'Org', 'G', 'Pink'], '40640', desc="Maddison/Wabash")
tn.add_station('Brn_40640', {'Org_40640':wait_time, 'P_40640':wait_time, 'Pink_40640':wait_time, 'G_40640':wait_time, 'Brn_40200':1, }, desc='Maddison/Wabash') # done
tn.add_station('P_40640', {'Org_40640':wait_time, 'Pink_40640':wait_time, 'Brn_40640':wait_time, 'G_40640':wait_time, 'P_40680':1, }, desc='Maddison/Wabash') # done
tn.add_station('Org_40640', {'P_40640':wait_time, 'Pink_40640':wait_time, 'Brn_40640':wait_time, 'G_40640':wait_time, 'Org_40680':1, }, desc='Maddison/Wabash') # done
tn.add_station('G_40640', {'Org_40640':wait_time, 'P_40640':wait_time, 'Pink_40640':wait_time, 'Brn_40640':wait_time, 'G_40680':1, 'G_40200':1, }, desc='Maddison/Wabash') # done
tn.add_station('Pink_40640', {'Org_40640':wait_time, 'P_40640':wait_time, 'Brn_40640':wait_time, 'G_40640':wait_time, 'Pink_40680':1, }, desc='Maddison/Wabash')  # done

#>>> trans(['Brn', 'P', 'Org', 'G', 'Pink'], '40200', desc="Randolph/Wabash")
tn.add_station('Brn_40200', {'G_40200':wait_time, 'P_40200':wait_time, 'Org_40200':wait_time, 'Pink_40200':wait_time, 'Brn_40260':1, }, desc='Randolph/Wabash') # done
tn.add_station('P_40200', {'Brn_40200':wait_time, 'G_40200':wait_time, 'Org_40200':wait_time, 'Pink_40200':wait_time, 'P_40640':1, }, desc='Randolph/Wabash') # done
tn.add_station('Org_40200', {'Brn_40200':wait_time, 'G_40200':wait_time, 'P_40200':wait_time, 'Pink_40200':wait_time, 'Org_40640':1, }, desc='Randolph/Wabash') # done
tn.add_station('G_40200', {'Brn_40200':wait_time, 'P_40200':wait_time, 'Org_40200':wait_time, 'Pink_40200':wait_time, 'G_40640':1,  'G_40260':1, }, desc='Randolph/Wabash') # done
tn.add_station('Pink_40200', {'Brn_40200':wait_time, 'G_40200':wait_time, 'P_40200':wait_time, 'Org_40200':wait_time, 'Pink_40640':1 }, desc='Randolph/Wabash') # done

#>>> trans(['Brn', 'P', 'Org', 'G', 'Pink'], '40260', desc="State/Lake")
tn.add_station('Brn_40260', {'G_40260':wait_time, 'Org_40260':wait_time, 'Pink_40260':wait_time, 'P_40260':wait_time, 'Red_41660':wait_time, 'Brn_40380':1 }, desc='State/Lake')  # done
tn.add_station('P_40260', {'G_40260':wait_time, 'Org_40260':wait_time, 'Pink_40260':wait_time, 'Brn_40260':wait_time, 'Red_41660':wait_time, 'P_40200':1, }, desc='State/Lake')  # done
tn.add_station('Org_40260', {'G_40260':wait_time, 'Pink_40260':wait_time, 'Brn_40260':wait_time, 'P_40260':wait_time, 'Red_41660':wait_time, 'Org_40200':1 }, desc='State/Lake')  # done
tn.add_station('G_40260', {'Org_40260':wait_time, 'Pink_40260':wait_time, 'Brn_40260':wait_time, 'P_40260':wait_time, 'Red_41660':wait_time, 'G_40200':1, 'G_40380':1 }, desc='State/Lake') # done
tn.add_station('Pink_40260', {'G_40260':wait_time, 'Org_40260':wait_time, 'Brn_40260':wait_time, 'P_40260':wait_time, 'Red_41660':wait_time, 'Pink_40200':1 }, desc='State/Lake')  # done

#>>> trans(['Brn', 'P', 'Org', 'G', 'Blue', 'Pink'], '40380', desc="Clark/Lake")
tn.add_station('Brn_40380', {'Blue_40380':wait_time, 'Pink_40380':wait_time, 'Org_40380':wait_time, 'G_40380':wait_time, 'P_40380':wait_time, 'Brn_40460':4, }, desc='Clark/Lake')  # done
tn.add_station('P_40380', {'Blue_40380':wait_time, 'Brn_40380':wait_time, 'Pink_40380':wait_time, 'Org_40380':wait_time, 'G_40380':wait_time, 'P_40260':1, }, desc='Clark/Lake')  # done
tn.add_station('Org_40380', {'Blue_40380':wait_time, 'Brn_40380':wait_time, 'Pink_40380':wait_time, 'G_40380':wait_time, 'P_40380':wait_time, 'Org_40260':1, }, desc='Clark/Lake')  # done
tn.add_station('G_40380', {'Blue_40380':wait_time, 'Brn_40380':wait_time, 'Pink_40380':wait_time, 'Org_40380':wait_time, 'P_40380':wait_time, 'G_40260': 1, 'G_41160':2 }, desc='Clark/Lake')  # done
tn.add_station('Blue_40380', {'Brn_40380':wait_time, 'Pink_40380':wait_time, 'Org_40380':wait_time, 'G_40380':wait_time, 'P_40380':wait_time, 'Blue_40490':2, 'Blue_40370':2 }, desc='Clark/Lake') # done
tn.add_station('Pink_40380', {'Blue_40380':wait_time, 'Brn_40380':wait_time, 'Org_40380':wait_time, 'G_40380':wait_time, 'P_40380':wait_time, 'Pink_40260':1, }, desc='Clark/Lake') # done

#>>> trans(['Red', 'Org', 'G', ], '41400', desc="Roosevelt")
tn.add_station('Red_41400', {'Org_41400':wait_time, 'G_41400':wait_time, }, desc='Roosevelt')
tn.add_station('Org_41400', {'Red_41400':wait_time, 'G_41400':wait_time, 'Org_40850':3 }, desc='Roosevelt')  # done loop
tn.add_station('G_41400', {'Org_41400':wait_time, 'Red_41400':wait_time, 'G_40680':3, }, desc='Roosevelt')  # done loop

#>>> trans(['Pink', 'G', ], '41160', desc="Clinton")
tn.add_station('Pink_41160', {'G_41160':wait_time, 'Pink_40380':2, }, desc='Clinton') # done loop
tn.add_station('G_41160', {'Pink_41160':wait_time, 'G_40380':2, }, desc='Clinton') # done loop

# Harrison Red
tn.add_station('Red_41490', { 'Red_41400':1, 'Red_40560':1 }, desc='Harrison')  # done

# Jackson Red
tn.add_station('Red_40560', { 'Red_41490':1, 'Red_41090':2, 'Blue_40070':red_blue_jackson_wait_time, 'Brn_40850':redlib_wait_time, 'P_40850':redlib_wait_time, 'Org_40850':redlib_wait_time, 'Pink_40850':redlib_wait_time }, desc='Jackson')  # done

# Monroe Red
tn.add_station('Red_41090', { 'Red_40560':2, 'Red_41660':1 }, desc='Monroe')  # done

# Lake Red 
tn.add_station('Red_41660', { 'Red_41090':1, 'Red_40330':1,'Brn_40260':wait_time, 'P_40260':wait_time, 'Org_40260':wait_time, 'G_40260':wait_time, 'Pink_40260':wait_time, }, desc='Lake Red')  # done 

# Grand Red
tn.add_station('Red_40330', { 'Red_41660':1, }, desc='Grand Red')  # done loop

# Grand Blue
tn.add_station('Blue_40490', { 'Blue_40380':2, }, desc='Grand Blue')  # done loop

# Washington Blue
tn.add_station('Blue_40370', { 'Blue_40380':2, 'Blue_41330':1 }, desc='Washington')  # done

# Monroe Blue
tn.add_station('Blue_41330', { 'Blue_40070':1, 'Blue_40370':1 }, desc='Monroe')  # done

# Jackson Blue
tn.add_station('Blue_40070', { 'Blue_41330':1, 'Blue_41340':1, 'Red_40560':red_blue_jackson_wait_time, 'Brn_40850':bluelib_wait_time, 'P_40850':bluelib_wait_time, 'Org_40850':bluelib_wait_time, 'Pink_40850':bluelib_wait_time}, desc='Jackson')  # done

# VanBuren Blue
tn.add_station('Blue_41340', { 'Blue_40070':1, }, desc='VanBuren')  # done loop


tn.shortest_path('Red_40330', 'Red_41400')



##################################################

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




tn = TransitNetwork() 
tn.add_station('red_a', {'red_b':1, })
tn.add_station('red_b', {'red_a':1, 'red_c':1,} )
tn.add_station('red_c', {'red_b':1, 'red_d':1,} )
tn.add_station('red_d', {'red_c':1, } )
tn.shortest_path('red_a', 'red_d')