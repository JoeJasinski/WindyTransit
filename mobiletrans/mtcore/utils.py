import decimal, urllib
from django.contrib.gis.geos import fromstr


def get_pt_from_coord(lat_input, long_input):

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


def get_distance(distance="806", distance_unit='m'):

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


def encode_args(url_parts):
    encoded = urllib.urlencode(url_parts)
    return encoded 
    
def build_url(protocol="http", host='example.com', path="/", args=""):
    return urllib.quote_plus("%s://%s%s?%s" % (protocol, host, path, args))
    