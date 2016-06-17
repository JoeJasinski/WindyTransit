from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import (
    Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon)
from django.contrib.gis.gdal.error import OGRIndexError
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import ShapeFileImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import *


class CityBorder(ShapeFileImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.CityBorder

    def get_geom_field(self):
        return "area"

    def parse_row(self, row):

        existing = False

        try:
            primary_key = row.get("OBJECTID")
        except OGRIndexError as error:
            raise ImportException("primary key 'OBJECTID' not available", error)

        try:
            cityborder = self.get_model_class().objects.get(objectid=primary_key)
            existing = True
        except ObjectDoesNotExist:
            cityborder = self.get_model_class()(objectid=primary_key)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with OBJECTID %s " % primary_key)

        try:
            cityborder.name = row.get("NAME")
        except OGRIndexError as error:
            raise ImportException("field 'NAME' not available", error)

        try:
            cityborder.shape_area = row.get("SHAPE_AREA")
        except OGRIndexError as error:
            raise ImportException("field 'SHAPE_AREA' not available", error)

        try:
            cityborder.shape_len = row.get("SHAPE_LEN")
        except OGRIndexError as error:
            raise ImportException("field 'SHAPE_LEN' not available", error)

        try:
            geom = row.geom
            geom.transform(self.coord_transform)
            cityborder.area = geom.wkt
        except Exception, error:
            raise ImportException("attribute 'geom' not available", error)

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1

        return cityborder
