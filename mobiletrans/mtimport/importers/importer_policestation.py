from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import JSONImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import *


class PoliceStation(JSONImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.PoliceStation

    def parse_row(self, row):

        existing = False

        try:
            uuid = row[1]
        except IndexError as error:
            raise IndexError("id %s: uuid %s" % (id, error))

        try:
            policestation = self.get_model_class().objects.get(uuid=uuid)
            existing = True
        except ObjectDoesNotExist:
            policestation = self.get_model_class()(uuid=uuid)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with uuid %s " % uuid)

        try:
            district = row[0]
        except IndexError as error:
            raise IndexError("id %s: district %s" % (id, error))
        policestation.district = district
        policestation.name = district

        try:
            address = row[9]
        except IndexError as error:
            raise IndexError("id %s: address %s" % (id, error))
        policestation.address = address

        try:
            zip = row[12]
        except IndexError as error:
            raise IndexError("id %s: zip %s" % (id, error))
        policestation.zip = zip

        try:
            website = row[13][0]
        except IndexError as error:
            raise IndexError("id %s: website %s" % (id, error))
        policestation.website = website

        try:
            lattitude = row[14][1]
        except IndexError as error:
            raise IndexError("id %s: lattitude %s" % (id, error))

        try:
            longitude = row[14][2]
        except IndexError as error:
            raise IndexError("id %s: longitude %s" % (id, error))

        point = fromstr('POINT(%s %s)' % (longitude, lattitude))
        policestation.point = point

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1

        return policestation
