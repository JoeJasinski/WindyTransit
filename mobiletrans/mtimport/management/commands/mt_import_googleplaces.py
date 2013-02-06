import os, json
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from mobiletrans.mtimport.importers import importer_googleplace as importer

class Command(BaseCommand):
    args = '<radius:lattitude:longitude>'
    help = 'Import Google Places given a lattitude and longitude and radius (in meters)'

    def handle(self, radius_lattitude_longitude="", **options):
    	radius, lattitude, longitude = radius_lattitude_longitude.split(":")
        if not (lattitude and longitude and radius):
            raise Exception("Lattitude and Longitude must be provided")
        self.stdout.write("Import Places from Lat: %s Long %s with radius %s\n" % (lattitude, longitude, radius))
        input_record = importer.GPlaceLocation.data_import({'lat':lattitude, 'lng':longitude,}, radius)
   
        self.stdout.write('Import completed with status: %s\n' % input_record.get_status_display())
