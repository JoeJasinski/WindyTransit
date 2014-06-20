import os
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from mobiletrans.mtdistmap.area_grid import RouteGridGenerator, RouteGridPoint, RouteGrid
from mobiletrans.mtlocation.models import CityBorder


class Command(BaseCommand):

    args = '<stop_id stop_id ...>'
    help = 'Generates a shapefile for the given transit stop ids.'

    option_list = BaseCommand.option_list + (
                                             
        make_option('--output-dir', '-o',
            action='store',
            dest='output_dir',
            default=False,
            help='Specify a shapefile export directory.'),

        make_option('--max-distance', '-d',
            action='store',
            dest='max_distance',
            default=2000,
            help='Max distance in meters consider close enough to a train stop. (default 2000)'),

        make_option('--num-routes', '-n',
            action='store',
            dest='num_routes',
            default=3,
            help='Given a point on the map, look for the x closest routes (default 3).'),
        
    )


    def handle(self, *args, **options):
        
        try:
            max_distance = int(options['max_distance'])
            self.stdout.write("max_distance set to {0}".format(max_distance))
        except (ValueError, TypeError) as e:
            self.stdout.write("--max-distance must be an integer", ending='')
            exit(1)

        try:
            num_routes = int(options['num_routes'])
            self.stdout.write("num_routes set to {0}".format(num_routes))
        except (ValueError, TypeError) as e:
            self.stdout.write("--num-routes must be an integer", ending='')
            exit(1)

        self.stdout.write("Looking up the city border.")
        region = CityBorder.objects.all()[0]
        center = region.area.centroid
        self.stdout.write("  City Center at {0}".format(center))
        grid = RouteGrid(xint=300, yint=300)
        
        for stop_id in args:
            self.stdout.write("Generating heatmap for {0}".format(stop_id))
            gridgen = RouteGridGenerator(stop_id, region, grid, max_distance=max_distance, num_routes=max_distance)
            self.stdout.write("Starting Calculation")
            g = gridgen.run(RouteGridPoint(0,0,center))
            self.stdout.write("Exporting to shapefile")
            shpfile = 'shapefiles/chicago_routegrid_{0}'.format(stop_id)
            g.generate_shapefile(shpfile)
            self.stdout.write("  File located at {0}".format(shpfile))
            
            
            