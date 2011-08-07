import json, csv
from django.db import models as dj_models
from mtimport import models
from django.contrib.gis.geos import Point, fromstr, fromfile
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ImportException(Exception):
    pass


class LocationBase(object):

    def __init__(self, input_record, input_data, loc_model):
        self.stats = {'new':0, 'existing':0, 'errors':0}
        
        self.input_record = input_record
        self.input_data = input_data
        self.loc_model = loc_model

    def process(self):

        for row in self.get_iteration_root():
            
            try:
                location = self.parse_row(row)
            except ValueError, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="ValueError Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except IndexError, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="IndexError Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except ImportException, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Import Exception Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except Exception, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Unknown Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)               
            else:
                location.save()
        
        return self.stats


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


    @classmethod
    def data_import(cls, input_file_path, input_record):
        
        status=None
        
        try:
            input_file = open(input_file_path,'r')
            input_data = json.load(input_file)
        except IOError:
            models.InputRecord.objects.make_note(
             input_record=input_record,
             note='Invalid File %s' % input_file_path,
             type=models.TRANSFER_NOTE_STATUS_ERROR,
            )
            models.InputRecord.objects.end_import(input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("Error with file read")
        except ValueError:
            models.InputRecord.objects.make_note(
             input_record=input_record,
             note='Invalid JSON %s' % input_file_path,
             type=models.TRANSFER_NOTE_STATUS_ERROR,
            )
            models.InputRecord.objects.end_import(input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("Error with JSON read")
        except Exception, error:
            models.InputRecord.objects.make_note(
             input_record=input_record,
             note='Unexpected problem %s: %s' % (input_file_path, error),
             type=models.TRANSFER_NOTE_STATUS_ERROR,
            )
            models.InputRecord.objects.end_import(input_record, models.TRANSFER_STATUS_FAILED)  
            raise ImportException("Unknown import error.")
        else:
            input_file.close()
    
        loc_model = dj_models.get_model('mtlocation', input_record.type) 
        locations = cls(input_record, input_data, loc_model)
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
        

class CSVLocationBase(LocationBase):
 
    def get_iteration_root(self):
        return self.input_data

    @classmethod
    def data_import(cls, input_file_path, input_record):
        
        status=None
        data = []
        try:
            input_file = open(input_file_path,'r')
            input_data = csv.reader(input_file, delimiter=',', quotechar='"')
            for row in input_data:
                data.append(row)
            data = data[1:]
        except IOError:
            models.InputRecord.objects.make_note(
             input_record=input_record,
             note='Invalid File %s' % input_file_path,
             type=models.TRANSFER_NOTE_STATUS_ERROR,
            )
            models.InputRecord.objects.end_import(input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("Error with file read")
        except Exception, error:
            models.InputRecord.objects.make_note(
             input_record=input_record,
             note='Unexpected problem %s: %s' % (input_file_path, error),
             type=models.TRANSFER_NOTE_STATUS_ERROR,
            )
            models.InputRecord.objects.end_import(input_record, models.TRANSFER_STATUS_FAILED)  
            raise ImportException("Unknown import error.")
        else:
            input_file.close()
    
        loc_model = dj_models.get_model('mtlocation', input_record.type) 
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

########################################

class Landmark(JSONLocationBase):
    
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

    
