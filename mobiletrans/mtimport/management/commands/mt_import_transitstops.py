import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from mobiletrans.mtimport.importers import importer_transitstop as importer

class Command(BaseCommand):
    args = '<stops.txt>'
    help = 'Import Stops'

    def handle(self, input_file_path="", **options):
        if not input_file_path:
            input_file_path = "%s" % os.path.join(settings.ENVIRONMENT_ROOT, "data", "cta", "stops.txt")
        self.stdout.write("Import %s \n" % input_file_path)
        input_record = importer.TransitStop.data_import(input_file_path)
        print input_file_path 


        self.stdout.write('Import completed with status: %s\n' % input_record.get_status_display())
