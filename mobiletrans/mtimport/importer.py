import json, csv, logging
from xml.dom import minidom
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models as dj_models

from autoslug.settings import slugify
from mobiletrans.mtimport import models
from mobiletrans.mtlocation import models as loc_models

class ImportException(Exception):
    pass

class IOImportException(Exception):
    pass

class DataFormatImportException(Exception):
    pass


class LocationBase(object):

    def __init__(self, input_record, input_data, loc_model):

        self.stats = {'new':0, 'existing':0, 'errors':0}
        
        self.input_record = input_record
        self.input_data = input_data
        self.loc_model = loc_model


    @classmethod
    def get_model_class(cls,):
        raise NotImplementedError("implement this get_model_class method in a subclass")

    @classmethod
    def data_import(cls, input_file_path):
        
        data = []
        status=None

        input_record = models.InputRecord()
        input_record.type = cls.get_model_class().__name__
        input_record.save()

        try:
            data = self.open_data(input_file_path)
        except ImportException, error:
            models.InputRecord.objects.make_note(
             input_record=input_record,
             note='Data Error: %s' % (error.message),
             type=models.TRANSFER_NOTE_STATUS_ERROR,
             exception=error.__class__.__name_,
            )
            models.InputRecord.objects.end_import(input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("Data load problem: %s" % (error))

    
        #loc_model = dj_models.get_model('mtlocation', input_record.type) 
        loc_model = cls.get_model_class()
        locations = cls(input_record, data, loc_model)
        stats = locations.process()
    
        
        if not input_record.status == models.TRANSFER_STATUS_FAILED:
            if input_record.inputnote_set.filter(type__in=[models.TRANSFER_NOTE_STATUS_ERROR,]):
                status = models.TRANSFER_STATUS_PARTIAL
            else:
                status = models.TRANSFER_STATUS_SUCCESS
                
        models.InputRecord.objects.make_note(
         input_record=input_record,
         note='# new records %s - # existing records %s - error records %s' % (
                                stats['new'], stats['existing'], stats['errors']),
         type=models.TRANSFER_NOTE_STATUS_NOTE,
        )     
            
        models.InputRecord.objects.end_import(input_record, status)

        return input_record
        

    def process(self):

        count = 1
        for row in self.get_iteration_root():
            
            try:
                location = self.parse_row(row)
            except ValueError, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Row %s: ValueError Parse error: %s" % (count, error),
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except IndexError, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Row %s: IndexError Parse error: %s" % (count, error),
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except ImportException, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Row %s: Import Exception Parse error: %s" % (count, error),
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except Exception, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Row %s: Unknown Parse error: %s" % (count, error),
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)               
            else:
                try:
                    location.save()
                except Exception, error: 
                    models.InputRecord.objects.make_note(
                     input_record=self.input_record,
                     note="Row %s: Save Error: %s" % (count, error),
                     type=models.TRANSFER_NOTE_STATUS_ERROR,    
                     )
                    self.stats['errors'] += 1                    

            count += 1

        return self.stats


    def get_iteration_root(self):
        raise NotImplementedError("implement this get_iteration_root method in a subclass")


    def open_data(self, input_file_path):
        raise NotImplementedError("implement this open_data method in a subclass")


    def parse_row(self, row):
        raise NotImplementedError("implement this parse_row method in a subclass")


class JSONLocationBase(LocationBase):

    def get_iteration_root(self):
        if self.input_data.has_key('data'):
            data = self.input_data['data']
        else:
            models.InputRecord.objects.make_note(
             input_record=self.input_record,
             note="Input file missing 'data' element.",
             type=models.TRANSFER_NOTE_STATUS_ERROR,    
             )
            models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("JSON missing 'data' element.")     
        return data


    def open_data(self, input_file_path):

        try:
            input_file = open(input_file_path,'r')
            input_data = json.load(input_file)
        except IOError, error:
            raise IOImportException("Error with file read: %s - %s" % (input_file_path, error.message, ))
        except ValueError:
            raise DataFormatImportException("Error with JSON read: %s - %s" % (input_file_path, error.message, ))
        except Exception, error:
            raise ImportException("Unknown import error: %s - %s" % (input_file_path, error.message, ))
        else:
            input_file.close()
        return input_data


class CSVLocationBase(LocationBase):
 
    def get_iteration_root(self):
        return self.input_data

    def open_data(self, input_file_path):

        try:
            input_file = open(input_file_path,'r')
            input_data = csv.reader(input_file, delimiter=',', quotechar='"')
            for row in input_data:
                data.append(row)
            data = data[1:]
        except IOError, error:
            raise IOImportException("Error with file load %s - %s" % (input_file_path, error.message))
        except Exception, error:
            raise ImportException("Unknown import error: %s - %s" % (input_file_path, error.message, ))
        else:
            input_file.close()
        return data


class KMLLocationBase(LocationBase):

    def get_iteration_root(self):

        placemarks = self.input_data.getElementsByTagName("Placemark")

        if not placemarks:            
            models.InputRecord.objects.make_note(
             input_record=self.input_record,
             note="Missing 'Placemark' elements.",
             type=models.TRANSFER_NOTE_STATUS_ERROR,    
             )
            models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("Missing 'Placemark' elements.")  

        return placemarks

    def open_data(self, input_file_path):

        try:
            input_file = open(input_file_path,'r')
            input_data = minidom.parse(input_file)
        except IOError, error:
            raise IOImportException("Error with file read: %s - %s" % (input_file_path, error.message, ))
        except ValueError:
            raise DataFormatImportException("Error with KML read: %s - %s" % (input_file_path, error.message, ))
        except Exception, error:
            raise ImportException("Unknown import error: %s - %s" % (input_file_path, error.message, ))
        else:
            input_file.close()
        return input_data



########################################

class Landmark(JSONLocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Landmark

    def parse_row(self, row):
        
        existing = False
        
        try:
            id = row[0]
        except IndexError, error:
            raise IndexError("id %s" % error)
        
        try:
            uuid = row[1]
        except IndexError, error:
            raise IndexError("id %s: uuid %s" % (id, error))
        
        try:
            landmark = self.loc_model.objects.get(uuid=uuid)
            existing = True
        except ObjectDoesNotExist:
            landmark = self.loc_model(uuid=uuid)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with uuid %s " % uuid)
        
        try:
            name = row[8]
        except IndexError, error:
            raise IndexError("id %s: name %s" % (id, error))
        landmark.name = name
        
        try:
            address = row[9]
        except IndexError, error:
            raise IndexError("id %s: address %s" % (id, error))
        landmark.address = address
        
        try:  
            created_date = row[10]
        except IndexError, error:
            raise IndexError("id %s: created_date %s" % (id, error))
        
        try:
            architect = row[11]
        except IndexError, error:
            raise IndexError("id %s: architect %s" % (id, error)) 
        landmark.architect = architect
        
        try:      
            lattitude = row[13]
        except IndexError, error:
            raise IndexError("id %s: lattitude %s" % (id, error)) 
        
        try:      
            longitude = row[14]
        except IndexError, error:
            raise IndexError("id %s: longitude %s" % (id, error))

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        landmark.point = point
        
        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        
        return landmark
    

class Library(JSONLocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Library

    def parse_row(self, row):
        
        existing = False
        
        try:
            id = row[0]
        except IndexError, error:
            raise IndexError("id %s" % error)
        
        try:
            uuid = row[1]
        except IndexError, error:
            raise IndexError("id %s: uuid %s" % (id, error))
        
        try:
            library = self.loc_model.objects.get(uuid=uuid)
            existing = True
        except ObjectDoesNotExist:
            library = self.loc_model(uuid=uuid)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with uuid %s " % uuid)
        
        try:
            name = row[8]
        except IndexError, error:
            raise IndexError("id %s: name %s" % (id, error))
        library.name = name

        try:
            hours = row[9]
        except IndexError, error:
            raise IndexError("id %s: address %s" % (id, error))
        library.hours = hours
                
        try:
            address = row[10]
        except IndexError, error:
            raise IndexError("id %s: address %s" % (id, error))
        library.address = address
 
        try:
            zip = row[13]
        except IndexError, error:
            raise IndexError("id %s: address %s" % (id, error))
        library.zip = zip 
        
        try:
            phone = row[14]
        except IndexError, error:
            raise IndexError("id %s: address %s" % (id, error))
        library.phone = phone 
        
        try:
            website = row[15][0]
        except IndexError, error:
            raise IndexError("id %s: address %s" % (id, error))
        library.website = website 
        
        try:      
            lattitude = row[16][1]
        except IndexError, error:
            raise IndexError("id %s: lattitude %s" % (id, error)) 
        
        try:      
            longitude = row[16][2]
        except IndexError, error:
            raise IndexError("id %s: longitude %s" % (id, error))

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        library.point = point
        
        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        
        return library


class TransitRoute(CSVLocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.TransitRoute

    def parse_row(self, row):
        row = list(row)
        existing = False
        
        pk = "route_id"          
        try:
            pk_val = row[0]
        except IndexError, error:
            raise IndexError("%s %s" % (pk, error))
        
        try:
            transitroute = self.loc_model.objects.get(route_id=pk_val)
            existing = True
        except ObjectDoesNotExist:
            transitroute = self.loc_model(route_id=pk_val)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        attr = (1, 'short_name')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (2, 'long_name')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (3, 'type')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (4, 'url')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (5, 'color')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        attr = (6, 'text_color')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        setattr(transitroute, attr[1], value) 

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        print(vars(transitroute))
        return transitroute


class TransitStop(CSVLocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.TransitStop

    def parse_row(self, row):
        row = list(row)
        existing = False
        
        pk = "stop_id"          
        try:
            pk_val = row[0]
        except IndexError, error:
            raise IndexError("%s %s" % (pk, error))
        
        try:
            transitstop = self.loc_model.objects.get(stop_id=pk_val)
            existing = True
        except ObjectDoesNotExist:
            transitstop = self.loc_model(stop_id=pk_val)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        #attr = (1, 'stop_code')
        #try:
        #    value = row[attr[0]]
        #except IndexError, error:
        #    raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        #setattr(transitstop, attr[1], value) 
        
        attr = (2, 'name')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error))  
        setattr(transitstop, attr[1], value)  
            
        attr = (3, 'lattitude')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        lattitude = value
        
        attr = (4, 'longitude')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error)) 
        longitude = value 
        
        attr = (5, 'location_type')
        try:
            value = row[attr[0]]
        except IndexError, error:
            raise IndexError("%s %s: %s %s" % (pk, pk_val, attr[1], error))  
        setattr(transitstop, attr[1], value)  

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        transitstop.point = point

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        print vars(transitstop)
        return transitstop


class Hospital(KMLLocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Hospital
   
    def parse_row(self, row):
        existing = False

        pk = "name"                 
        try:
            pk_val = row.getElementsByTagName(pk)[0]
        except Exception, error:
            raise IndexError("%s %s" % (pk, error))

        try:
            pk_text = pk_val.childNodes[0].nodeValue
        except Exception, error:
            raise Exception("%s %s: Error Reading 'text' from 'pk': %s" % (pk, pk_val, error)) 

        slug = slugify(pk_text)
        
        try:
            hospital = self.loc_model.objects.get(slug=slug)
            existing = True
        except ObjectDoesNotExist:
            hospital = self.loc_model(slug=slug)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        hospital.name = pk_text
        

        try:
            point = row.getElementsByTagName("Point")[0]
        except Exception, error:
            raise IndexError("%s %s: Error Reading 'Point' from 'Placemark': %s" % (pk, pk_val, error)) 
        
        try:       
            coordinates = point.getElementsByTagName("coordinates")[0]
        except Exception, error:        
            raise Exception("%s %s: Error Reading 'coordinates' from 'Point': %s" % (pk, pk_val, error)) 
        
        try:
            coord_text = coordinates.childNodes[0].nodeValue
        except Exception, error:
            raise Exception("%s %s: Error Reading 'text' from 'coordinates': %s" % (pk, pk_val, error)) 
        
        try:
            longitude, lattitude, other =  coord_text.split(',')
        except Exception, error:
            raise Exception("%s %s: Error splitting 'text': %s" % (pk, pk_val, error)) 
        

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        hospital.point = point     

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        print vars(hospital)
        return hospital
    

class GPlaceLocationBase(LocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.GPlace

    def get_iteration_root(self):
        if hasattr(self.input_data, 'places'):
            data = self.input_data.places
        else:
            models.InputRecord.objects.make_note(
             input_record=self.input_record,
             note="Input file missing 'places' element.",
             type=models.TRANSFER_NOTE_STATUS_ERROR,    
             )
            models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("JSON missing 'places' element.")     
        return data

    def parse_row(self, row):
        
        existing = False
        
        try:
            id = row.id
        except AttributeError, error:
            raise AttributeError("id %s" % error)
        
        try:
            uuid = row.id
        except AttributeError, error:
            raise AttributeError("id %s: uuid %s" % (id, error))
        
        try:
            place = self.loc_model.objects.get(uuid=uuid) 
            existing = True
        except ObjectDoesNotExist:
            place = self.loc_model(uuid=uuid)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with uuid %s " % uuid)
       
        try:
            name = row.name
        except AttributeError, error:
            raise AttributeError("id %s: name %s" % (id, error))
        place.name = name

        try:
            geo = row.geo_location
        except AttributeError, error:
            raise AttributeError("id %s: geo_location %s" % (id, error))
        else:
            if geo.has_key('lng'):
                longitude = geo['lng']
            else:
                raise AttributeError("id %s: geo_location.lng" % (id))

            if geo.has_key('lat'):
                lattitude = geo['lat']
            else:
                raise AttributeError("id %s: geo_location.lat " % (id ))

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        place.point = point
 
        if hasattr(row, 'rating'):
            place.rating = row.rating 

        if hasattr(row, 'vicinity'):
            place.vicinity = row.vicinity

        if hasattr(row, 'types'):
            place.types = row.types

        if hasattr(row, 'reference'):
            place.reference = row.reference

        if hasattr(row, 'international_phone_number'):
            place.international_phone_number = row.international_phone_number

        if hasattr(row, 'local_phone_number'):
            place.local_phone_number = row.local_phone_number
 
        if hasattr(row, 'website'):
            place.website = row.website
 
        if hasattr(row, 'formatted_address'):
            place.address = row.formatted_address

        if hasattr(row, 'url'):
            place.url = row.url
     
        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        
        return place

    
class Neighborhood(KMLLocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Neighborhood

    def parse_row(self, row):
        existing = False

        pk = "name"                 
        try:
            pk_val = row.getElementsByTagName(pk)[0]
        except Exception, error:
            raise IndexError("%s %s" % (pk, error))

        try:
            pk_text = pk_val.childNodes[0].nodeValue
        except Exception, error:
            raise Exception("%s %s: Error Reading 'text' from 'pk': %s" % (pk, pk_val, error)) 

        slug = slugify(pk_text)
        
        try:
            neighborhood = self.loc_model.objects.get(slug=slug)
            existing = True
        except ObjectDoesNotExist:
            neighborhood = self.loc_model(slug=slug)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        neighborhood.name = pk_text
        
        
        try:
            description = row.getElementsByTagName("description")[0].childNodes[0].nodeValue
        except Exception, error:
            pass
        
        s2 = description.replace("\n","")
        s3 = s2[s2.find("PRI_NEIGH<"):]
        s4 = s3[:s3.find("SEC_NEIGH_NO")]
        s5 = s4.replace('<td>',"").replace('</td>','').replace("PRI_NEIGH",'').replace("</tr>",'').replace("<tr>",'')
        neighborhood.long_name = s5

        try:
            ring = row.getElementsByTagName("MultiGeometry")[0]
        except Exception, error:
            raise IndexError("%s %s: Error Reading 'MultiGeometry' from 'Placemark': %s" % (pk, pk_val, error)) 

        try:       
            coordinates = ring.getElementsByTagName("coordinates")[0]
        except Exception, error:        
            raise Exception("%s %s: Error Reading 'coordinates' from 'Point': %s" % (pk, pk_val, error)) 
        
        try:
            coord_text = coordinates.childNodes[0].nodeValue
        except Exception, error:
            raise Exception("%s %s: Error Reading 'text' from 'coordinates': %s" % (pk, pk_val, error)) 
        
        poly = coord_text.split(' ')
    
        
        point_str = ""
        for point in poly:
            if point: 
                try:
                    longitude, lattitude, other =  point.split(',')
                except Exception, error:
                    raise Exception("%s %s: Error splitting 'text': %s" % (pk, pk_val, error)) 
                point_str += "%s %s," % (longitude, lattitude)
        
        p =  GEOSGeometry('POLYGON((%s))' % point_str.strip()[:-1])
        neighborhood.area = p

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        print vars(neighborhood)
        return neighborhood
    
    
class Zipcode(KMLLocationBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Zipcode

    def parse_row(self, row):
        existing = False

        pk = "name"                 
        try:
            pk_val = row.getElementsByTagName(pk)[0]
        except Exception, error:
            raise IndexError("%s %s" % (pk, error))

        try:
            pk_text = pk_val.childNodes[0].nodeValue
        except Exception, error:
            raise Exception("%s %s: Error Reading 'text' from 'pk': %s" % (pk, pk_val, error)) 

        slug = slugify(pk_text)
        
        try:
            neighborhood = self.loc_model.objects.get(slug=slug)
            existing = True
        except ObjectDoesNotExist:
            neighborhood = self.loc_model(slug=slug)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        neighborhood.name = pk_text
        
        
        try:
            description = row.getElementsByTagName("description")[0].childNodes[0].nodeValue
        except Exception, error:
            pass
        
        s2 = description.replace("\n","")
        s3 = s2[s2.find("ZIP"):]
        s4 = s3[:s3.find("</table>")]
        s5 = s4.replace('<td>',"").replace('</td>','').replace("ZIP",'').replace("</tr>",'').replace("<tr>",'')
        neighborhood.long_name = s5

        try:
            ring = row.getElementsByTagName("MultiGeometry")[0]
        except Exception, error:
            raise IndexError("%s %s: Error Reading 'MultiGeometry' from 'Placemark': %s" % (pk, pk_val, error)) 

        try:       
            coordinates = ring.getElementsByTagName("coordinates")[0]
        except Exception, error:        
            raise Exception("%s %s: Error Reading 'coordinates' from 'Point': %s" % (pk, pk_val, error)) 
        
        try:
            coord_text = coordinates.childNodes[0].nodeValue
        except Exception, error:
            raise Exception("%s %s: Error Reading 'text' from 'coordinates': %s" % (pk, pk_val, error)) 
        
        poly = coord_text.split(' ')
    
        
        point_str = ""
        for point in poly:
            if point: 
                try:
                    longitude, lattitude, other =  point.split(',')
                except Exception, error:
                    raise Exception("%s %s: Error splitting 'text': %s" % (pk, pk_val, error)) 
                point_str += "%s %s," % (longitude, lattitude)
        
        p =  GEOSGeometry('POLYGON((%s))' % point_str.strip()[:-1])
        neighborhood.area = p

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        print vars(neighborhood)
        return neighborhood
