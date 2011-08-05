import json
from mtimport import models
from django.contrib.gis.geos import Point, fromstr, fromfile
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ImportException(Exception):
    pass


class Library(object):
    
    def __init__(self, input_record, input_data):
        self.stats = {'new':0, 'existing':0,}
        
        self.input_record = input_record
        self.input_data = input_data
    
    def process(self):
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
        
        for row in data:
            
            try:
                library = self.parse_row(row)
            except ValueError, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="ValueError JSON Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except IndexError, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="IndexError JSON Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except ImportException, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Import Exception JSON Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except Exception, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Unknown JSON Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)               
            else:
                library.save()
        
        return self.stats
        
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
        
        from mtlocation import models as loc_models
        try:
            library = loc_models.Library.objects.get(uuid=uuid)
            existing = True
        except ObjectDoesNotExist:
            library = loc_models.Library(uuid=uuid)
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

def data_import(input_file_path, input_record):
    
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

    libraries = Library(input_record, input_data)
    stats = libraries.process()
    
    
    if not input_record.status == models.TRANSFER_STATUS_FAILED:
        if input_record.inputnote_set.filter(type__in=[models.TRANSFER_NOTE_STATUS_ERROR,]):
            status = models.TRANSFER_STATUS_PARTIAL
        else:
            status = models.TRANSFER_STATUS_SUCCESS
            
    models.InputRecord.objects.make_note(
     input_record=input_record,
     note='# new records %s - # existing records %s' % (stats['new'], stats['existing']),
     type=models.TRANSFER_NOTE_STATUS_NOTE,
    )     
        
    models.InputRecord.objects.end_import(input_record, status)
    
    