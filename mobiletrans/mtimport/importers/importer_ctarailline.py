from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from django.contrib.gis.gdal.error import OGRIndexError
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import ShapeFileImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import * 

class CTARailLines(ShapeFileImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.CTARailLines

    def get_geo_field(self):
        return "line"

    def parse_row(self, row):
        
        existing = False

        try:
            primary_key = row.get("OBJECTID")
        except OGRIndexError, error:
            raise ImportException("primary key 'OBJECTID' not available", error)
        
        try:
            ctarailline = self.get_model_class().objects.get(objectid=primary_key)
            existing = True
        except ObjectDoesNotExist:
            ctarailline = self.get_model_class()(objectid=primary_key)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with OBJECTID %s " % primary_key)
        
        try:
            ctarailline.segment_id = row.get("SEGMENT_ID")
        except OGRIndexError, error:
            raise ImportException("field 'SEGMENT_ID' not available", error)

        try:
            ctarailline.asset_id = row.get("ASSET_ID")
        except OGRIndexError, error:
            raise ImportException("field 'ASSET_ID' not available", error)

        try:
            ctarailline.transit_lines = row.get("LINES")
        except OGRIndexError, error:
            raise ImportException("field 'LINES' not available", error)

        try:
            ctarailline.description = row.get("DESCRIPTIO")
        except OGRIndexError, error:
            raise ImportException("field 'DESCRIPTIO' not available", error)

        try:
            ctarailline.type = row.get("TYPE")
        except OGRIndexError, error:
            raise ImportException("field 'TYPE' not available", error)

        try:
            ctarailline.legend = row.get("LEGEND")
        except OGRIndexError, error:
            raise ImportException("field 'LEGEND' not available", error)

        try:
            ctarailline.alt_legend = row.get("ALT_LEGEND")
        except OGRIndexError, error:
            raise ImportException("field 'ALT_LEGEND' not available", error)

        try:
            ctarailline.branch = row.get("BRANCH")
        except OGRIndexError, error:
            raise ImportException("field 'BRANCH' not available", error)

        try:
            ctarailline.shape_len = row.get("SHAPE_LEN")
        except OGRIndexError, error:
            raise ImportException("field 'SHAPE_LEN' not available", error)            

        try:
            geom = row.geom
            geom.transform(self.coord_transform)
            ctarailline.line = geom.wkt
        except Exception, error:
            raise ImportException("attribute 'geom' not available", error)     
        
        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1
        
        return ctarailline