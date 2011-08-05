import csv
from mtimport import models
from django.contrib.gis.geos import Point, fromstr, fromfile
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

class ImportException(Exception):
    pass


class TransitRoute(object):
    
    def __init__(self, input_record, input_data):
        self.stats = {'new':0, 'existing':0,}
        
        self.input_record = input_record
        self.input_data = input_data
    
    def process(self):

        data = self.input_data

        for row in data:
            
            try:
                transitroute = self.parse_row(row)
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
                transitroute.save()
        
        return self.stats
        
    def parse_row(self, row):
        row = list(row)
        existing = False
        
        
        pk = "route_id"          
        try:
            pk_val = row[0]
        except IndexError, error:
            raise IndexError("%s %s" % (pk, error))
        
        
        from mtlocation import models as loc_models
        try:
            transitroute = loc_models.TransitRoute.objects.get(route_id=pk_val)
            existing = True
        except ObjectDoesNotExist:
            transitroute = loc_models.TransitRoute(route_id=pk_val)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with stop_id %s " % stop_id)

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
        
        return transitroute

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

    transitstop = TransitRoute(input_record, data)
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
    
    