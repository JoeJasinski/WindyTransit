import os, json
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from mobiletrans.mtimport.importers import importer_hospital as importer

class Command(BaseCommand):
    args = '<hostpitals.kml>'
    help = 'Import Landmarks'

    def handle(self, input_file_path="", **options):
        if not input_file_path:
            input_file_path = "%s" % os.path.join(settings.ENVIRONMENT_ROOT, "data", "hospitals.kml")
        self.stdout.write("Import %s \n" % input_file_path)
        input_record = importer.Hospital.data_import(input_file_path)
        print input_file_path 


        self.stdout.write('Import completed with status: %s\n' % input_record.get_status_display())
