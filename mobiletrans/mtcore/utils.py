import decimal, urllib
from django.apps import apps
from django.contrib.gis.geos import fromstr
from mobiletrans.mtlocation.models import Location


def encode_args(url_parts):
    encoded = urllib.urlencode(url_parts)
    return encoded 
    
def build_url(protocol="http", host='example.com', path="/", args="", encode=True):
    url = ("%s://%s%s?%s" % (protocol, host, path, args))
    if encode:
        url = urllib.quote_plus(url)
    return url

class PrepParams(object):

    def get_pt_from_coord(self, lat_input, long_input):
    
        lat = None   
        long = None
        if lat_input and long_input:
            try:
                lat = decimal.Decimal(lat_input)
            except decimal.InvalidOperation:
                pass
            
            try:
                long = decimal.Decimal(long_input)
            except decimal.InvalidOperation:
                pass
        
        if not lat:
            lat = "41.881944"
            
        if not long:
            long = "-87.627778"
    
        ref_pnt = fromstr('POINT(%s %s)' % (str(long), str(lat)))        

        return (ref_pnt, lat, long)
    
    
    def get_distance(self, distance="806", distance_unit='m'):
    
        if not distance_unit in ['km','mi','m','yd','ft',]:
            distance_unit = 'm'
            
        if distance:
            try:
                distance = decimal.Decimal("%s" % distance)
            except:
                pass
        
        if not distance:
            distance = "806"                  
        d = {str(distance_unit):str(distance)} 
        #raise Exception(d)     
        return d

    
    def get_point_types(self, point_types):
        available_types = [ (m.__name__).lower() for m in apps.get_app_config('mtlocation').get_models() if issubclass(m, Location)  ]
        point_types = map(lambda x: x.lower(), point_types)
        types = set(point_types).intersection(set(available_types))
        #raise AssertionError(available_types, point_types, types)
        return list(types)
    
    
    def get_neighborhood(self, neighborhood):
        if "%s".lower() % neighborhood in ['false','0',0,'no','n']:
            neighborhood  = False
        else:
            neighborhood = True
        return neighborhood
        

    def get_zipcode(self, zipcode):
        if "%s".lower() % zipcode in ['false','0',0,'no','n']:
            zipcode  = False
        else:
            zipcode = True
        return zipcode
    
    
    def get_limit(self, limit):
    
        if not limit:
            limit = 25
        else:
            try:
                limit = int(limit)
            except:
                limit = 25
            else:
                if limit < 1 or limit > 50:
                    limit = 25
            
        return limit


    def __init__(self, request, overrides={}):
        
        if overrides.has_key('lat'):
            lat = overrides['lat']
        else:
            lat = request.GET.get('lat')
            
        if overrides.has_key('long'):
            long = overrides['long']
        else:
            long = request.GET.get('long')
            if not long:
                long = request.GET.get('lon')
            if not long:
                long = request.GET.get('lng') 

                        
        ref_pnt, lat, long = self.get_pt_from_coord(lat, long)
    
        if overrides.has_key('du'):
            distance_unit = overrides['du']
        else:
            distance_unit = request.GET.get('du')
        
        if overrides.has_key('d'):
            distance = overrides['d']
        else:
            distance =  request.GET.get('d')
        d = self.get_distance(distance, distance_unit)
    
        if overrides.has_key('limit'):
            limit = overrides['limit']
        else:
            limit = request.GET.get('limit')
        limit = self.get_limit(limit)

        if overrides.has_key('neighborhood'):
            neighborhood = overrides['neighborhood']    
        else: 
            neighborhood = request.GET.get('neighborhood')
        neighborhood = self.get_neighborhood(neighborhood)

        if overrides.has_key('zipcode'):
            zipcode = overrides['zipcode']    
        else: 
            zipcode = request.GET.get('zipcode')
        zipcode = self.get_neighborhood(zipcode)


        if overrides.has_key('point_types'):
            point_types_input = overrides['point_types']
        else:   
            point_types_input = request.GET.getlist('type')
        point_types = self.get_point_types(point_types_input)

        self.lat = lat
        self.long = long
        self.distance_unit = distance_unit
        self.distance = distance
        self.d = d
        self.neighborhood = neighborhood
        self.zipcode = zipcode
        self.limit = limit
        self.point_types = point_types
        self.point_types_input = point_types_input
        self.ref_pnt = ref_pnt
    
