import csv
from mtimport import models
from django.contrib.gis.geos import Point, fromstr, fromfile
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ImportException(Exception):
    pass


class TransitStop(object):
    
    def __init__(self, input_record, input_data):
        self.stats = {'new':0, 'existing':0,}
        
        self.input_record = input_record
        self.input_data = input_data
    
    def process(self):

        data = self.input_data

        for row in data:
            
            try:
                transitstop = self.parse_row(row)
            except ValueError, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="ValueError Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except IndexError, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="IndexError Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except ImportException, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Import Exception Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except Exception, error:
                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Unknown Parse error: %s" % error,
                 type=models.TRANSFER_NOTE_STATUS_ERROR,    
                 )
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)               
            else:
                transitstop.save()
        
        return self.stats
        
    def parse_row(self, row):
        row = list(row)
        existing = False
        
        try:
            stop_id = row[0]
        except IndexError, error:
            raise IndexError("stop_id %s" % error)
        
        
        from mtlocation import models as loc_models
        try:
            transitstop = loc_models.TransitStop.objects.get(stop_id=stop_id)
            existing = True
        except ObjectDoesNotExist:
            transitstop = loc_models.TransitStop(stop_id=stop_id)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with stop_id %s " % stop_id)


        try:
            stop_code = row[1]
        except IndexError, error:
            raise IndexError("stop_id %s: stop_code %s" % (stop_id, error))
        transitstop.stop_code

        try:
            name = row[2]
        except IndexError, error:
            raise IndexError("stop_id %s: name %s" % (stop_id, error))
        transitstop.name = name
                
        try:
            lattitude = row[3]
        except IndexError, error:
            raise IndexError("stop_id %s: lattitude %s" % (stop_id, error)) 
        
        try:      
            longitude = row[4]
        except IndexError, error:
            raise IndexError("stop_id %s: longitude %s" % (stop_id, error))

        point = fromstr('POINT(%s %s)' % (lattitude, longitude))
        transitstop.point = point

        try:      
            location_type = row[5]
        except IndexError, error:
            raise IndexError("stop_id %s: location_type %s" % (stop_id, error))
        transitstop.location_type = location_type
       
        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        
        return transitstop

def data_import(input_file_path, input_record):
    
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

    transitstop = TransitStop(input_record, data)
    stats = transitstop.process()
    
    
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
    
    