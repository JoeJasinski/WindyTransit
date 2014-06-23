import os
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from mobiletrans.mtdistmap.cta_conn import load_transitnetwork


class Command(BaseCommand):

    args = '<stop_id stop_id >'
    help = 'caculates the shortest route between two transit stop ids.'
    
    def handle(self, *args, **options):

        if not len(args) == 2:
            self.stdout.write("2 args required")
            exit(1)
        tn = load_transitnetwork()
        sp = tn.shortest_path(args[0], args[1])
        if sp:
            self.stdout.write(str(sp.to_json()))
        else:
            self.stdout.write({'error':'no route'})