import json, csv, logging, traceback
from django.contrib.gis import gdal 
from xml.dom import minidom

from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import * 

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


class ImportBase(object):

    def __init__(self, input_record, input_data):

        self.stats = {'new':0, 'existing':0, 'errors':0}
        
        self.input_record = input_record
        self.input_data = input_data

    @classmethod
    def get_model_class(cls,):
        raise NotImplementedError("implement this get_model_class method in a subclass")

    @classmethod
    def data_import(cls, *input_parameters):
        
        data = []
        status=None

        input_record = models.InputRecord()
        input_record.type = cls.get_model_class().__name__
        input_record.save()

        try:
            data = cls.open_data(*input_parameters)
        except ImportException, error:

            stacktrace_file = StringIO()
            traceback.print_exc(limit=50, file=stacktrace_file)
            stacktrace_file.seek(0)
            stacktrace_text = stacktrace_file.read()

            models.InputRecord.objects.make_note(
             input_record=input_record,
             note='Data Error: %s\n\n%s' % (error, stacktrace_text),
             type=models.TRANSFER_NOTE_STATUS_ERROR,
             exception=error.__class__.__name__,
            )
            models.InputRecord.objects.end_import(input_record, models.TRANSFER_STATUS_FAILED)
            raise ImportException("Data load problem: %s" % (error))

        import_class = cls(input_record, data, )
        stats = import_class.process()
    
        
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
                import_object = self.parse_row(row)
            except ValueError, error:

                stacktrace_file = StringIO()
                traceback.print_exc(limit=50, file=stacktrace_file)
                stacktrace_file.seek(0)
                stacktrace_text = stacktrace_file.read()

                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Row %s: ValueError Parse error: %s\n\n%s" % (count, error, stacktrace_text),
                 type=models.TRANSFER_NOTE_STATUS_ERROR,
                 exception=error.__class__.__name__,
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except IndexError, error:

                stacktrace_file = StringIO()
                traceback.print_exc(limit=50, file=stacktrace_file)
                stacktrace_file.seek(0)
                stacktrace_text = stacktrace_file.read()

                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Row %s: IndexError Parse error: %s\n\n%s" % (count, error, stacktrace_text),
                 type=models.TRANSFER_NOTE_STATUS_ERROR,   
                 exception=error.__class__.__name__, 
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except ImportException, error:

                stacktrace_file = StringIO()
                traceback.print_exc(limit=50, file=stacktrace_file)
                stacktrace_file.seek(0)
                stacktrace_text = stacktrace_file.read()

                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Row %s: Import Exception Parse error: %s\n\n%s" % (count, error, stacktrace_text),
                 type=models.TRANSFER_NOTE_STATUS_ERROR, 
                 exception=error.__class__.__name__,  
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)
            except Exception, error:

                stacktrace_file = StringIO()
                traceback.print_exc(limit=50, file=stacktrace_file)
                stacktrace_file.seek(0)
                stacktrace_text = stacktrace_file.read()

                models.InputRecord.objects.make_note(
                 input_record=self.input_record,
                 note="Row %s: Unknown Parse error: %s\n\n%s" % (count, error, stacktrace_text),
                 type=models.TRANSFER_NOTE_STATUS_ERROR,
                 exception=error.__class__.__name__,    
                 )
                self.stats['errors'] += 1
                models.InputRecord.objects.end_import(self.input_record, models.TRANSFER_STATUS_FAILED)               
            else:
                try:
                    print "LOCATION", vars(import_object)
                    import_object.full_clean()
                    import_object.save()
                except Exception, error: 

                    stacktrace_file = StringIO()
                    traceback.print_exc(limit=50, file=stacktrace_file)
                    stacktrace_file.seek(0)
                    stacktrace_text = stacktrace_file.read()

                    models.InputRecord.objects.make_note(
                     input_record=self.input_record,
                     note="Row %s: Save Error: %s\n\n%s" % (count, error, stacktrace_text),
                     type=models.TRANSFER_NOTE_STATUS_ERROR,
                     exception=error.__class__.__name__,    
                     )
                    self.stats['errors'] += 1                    

            count += 1

        return self.stats


    def get_iteration_root(self):
        raise NotImplementedError("implement this get_iteration_root method in a subclass")


    def open_data(self, **input_parameters):
        raise NotImplementedError("implement this open_data method in a subclass")


    def parse_row(self, row):
        raise NotImplementedError("implement this parse_row method in a subclass")



########################################
# Format-Specific loader base classes
########################################

class JSONImportBase(ImportBase):

    @classmethod
    def open_data(cls, input_file_path):

        try:
            input_file = open(input_file_path,'r')
            input_data = json.load(input_file)
        except IOError, error:
            raise IOImportException("Error with file read: %s - %s" % (input_file_path, error, ))
        except ValueError:
            raise DataFormatImportException("Error with JSON read: %s - %s" % (input_file_path, error, ))
        except Exception, error:
            raise ImportException("Unknown import error: %s - %s" % (input_file_path, error, ))
        else:
            input_file.close()
        return input_data

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


class CSVImportBase(ImportBase):

    @classmethod
    def open_data(cls, input_file_path):

        try:
            input_file = open(input_file_path,'r')
            input_data = csv.reader(input_file, delimiter=',', quotechar='"')
            for row in input_data:
                data.append(row)
            data = data[1:]
        except IOError, error:
            raise IOImportException("Error with file load %s - %s" % (input_file_path, error))
        except Exception, error:
            raise ImportException("Unknown import error: %s - %s" % (input_file_path, error, ))
        else:
            input_file.close()
        return data
 
    def get_iteration_root(self):
        return self.input_data


class KMLImportBase(ImportBase):

    @classmethod
    def open_data(cls, input_file_path):

        try:
            input_file = open(input_file_path,'r')
            input_data = minidom.parse(input_file)
        except IOError, error:
            raise IOImportException("Error with file read: %s - %s" % (input_file_path, error, ))
        except ValueError:
            raise DataFormatImportException("Error with KML read: %s - %s" % (input_file_path, error, ))
        except Exception, error:
            raise ImportException("Unknown import error: %s - %s" % (input_file_path, error, ))
        else:
            input_file.close()
        return input_data

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



from django.db import connections, router

class ShapeFileImportBase(ImportBase):

    def get_geo_field(self):
        raise NotImplementedError("subclasses must implement this to specify a field name string of the geography field.")

    def prepare_srid_transform(self, source_srs, model_class, geo_field, ):
        using = router.db_for_write(model_class)
        spatial_backend = connections[using].ops
        opts = model_class._meta
        geo_field, model, direct, m2m = opts.get_field_by_name(geom_field)
        SpatialRefSys = spatial_backend.spatial_ref_sys()
        target_srs = SpatialRefSys.objects.using(using).get(srid=geo_field.srid).srs
        return gdal.CoordTransform(source_srs, target_srs)

    @classmethod
    def open_data(cls, input_file_path):

        try:
            input_data = gdal.DataSource(input_file_path)
        except IOError, error:
            raise IOImportException("Error with ShapeFile read: %s - %s" % (input_file_path, error, ))
        except gdal.error.OGRException:
            raise DataFormatImportException("Error with ShapeFile read: %s - %s" % (input_file_path, error, ))
        except Exception, error:
            raise ImportException("Unknown import ShapeFile error: %s - %s" % (input_file_path, error, ))
        return input_data

    def get_iteration_root(self):
        try:
            input_data = self.input_data[0]
        except IndexError, error:
            raise ImportException("Root element not found: %s"  % (error))  
        
        self.coord_transform = self.prepare_srid_transform(
                                    source_srs=input_data.srs, 
                                    model_class=self.get_model_class(),
                                    geo_field=self.get_geo_field(), 
                                    )
        return input_data

########################################


    