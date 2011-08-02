import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from mtimport import transitstop, models
from mtlocation import models as loc_models

class Command(BaseCommand):
    args = '<stops.txt>'
    help = 'Import Stops'

    def handle(self, input_file_path="", **options):
        if not input_file_path:
            input_file_path = "%s" % os.path.join(settings.VENV_ROOT, "data", "cta", "stops.txt")

        input_record = models.InputRecord()
        input_record.type = loc_models.TransitStop.__name__
        input_record.save()
        transitstop.data_import(input_file_path, input_record)
        print input_file_path 


        self.stdout.write('Import completed with status: %s\n' % input_record.get_status_display())