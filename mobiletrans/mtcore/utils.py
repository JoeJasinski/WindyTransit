import decimal
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
    
    if lat and long:
        ref_pnt = fromstr('POINT(%s %s)' % (str(lat), str(long)))
    else:
        ref_pnt =  fromstr('POINT(-87.627778 41.881944)')
    
    return (ref_pnt, lat, long)


def get_distance(distance, distance_unit):

    if not distance_unit in ['km','mi','m','yd','ft',]:
        distance_unit = 'm'
        
    if distance:
        try:
            distance = int(distance)
        except:
            pass
    
    if not distance:
        distance = 1000                    
    d = {distance_unit:distance}      
    return d