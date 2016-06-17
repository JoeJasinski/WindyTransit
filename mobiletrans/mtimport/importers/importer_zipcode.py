from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.contrib.gis.geos import Point, fromstr, fromfile, GEOSGeometry, MultiPoint, MultiPolygon, Polygon
from autoslug.settings import slugify
from mobiletrans.mtimport.importer import KMLImportBase
from mobiletrans.mtlocation import models as loc_models
from mobiletrans.mtimport import models
from mobiletrans.mtimport.exceptions import *


class Zipcode(KMLImportBase):

    @classmethod
    def get_model_class(cls,):
        return loc_models.Zipcode

    def parse_row(self, row):
        existing = False

        pk = "name"
        try:
            pk_val = row.getElementsByTagName(pk)[0]
        except Exception as error:
            raise IndexError("%s %s" % (pk, error))

        try:
            pk_text = pk_val.childNodes[0].nodeValue
        except Exception as error:
            raise Exception("%s %s: Error Reading 'text' from 'pk': %s" % (pk, pk_val, error))

        slug = slugify(pk_text)

        try:
            neighborhood = self.get_model_class().objects.get(slug=slug)
            existing = True
        except ObjectDoesNotExist:
            neighborhood = self.get_model_class()(slug=slug)
            existing = False
        except MultipleObjectsReturned:
            raise ImportException("multiple objects returned with %s %s " % (pk, pk_val))

        neighborhood.name = pk_text

        try:
            description = row.getElementsByTagName("description")[0].childNodes[0].nodeValue
        except Exception as error:
            pass

        s2 = description.replace("\n", "")
        s3 = s2[s2.find("ZIP"):]
        s4 = s3[:s3.find("</table>")]
        s5 = s4.replace('<td>', "").replace('</td>', '').replace("ZIP", '').replace("</tr>", '').replace("<tr>", '')
        neighborhood.long_name = s5

        try:
            ring = row.getElementsByTagName("MultiGeometry")[0]
        except Exception as error:
            raise IndexError("%s %s: Error Reading 'MultiGeometry' from 'Placemark': %s" % (pk, pk_val, error))

        try:
            coordinates = ring.getElementsByTagName("coordinates")[0]
        except Exception as error:
            raise Exception("%s %s: Error Reading 'coordinates' from 'Point': %s" % (pk, pk_val, error))

        try:
            coord_text = coordinates.childNodes[0].nodeValue
        except Exception as error:
            raise Exception("%s %s: Error Reading 'text' from 'coordinates': %s" % (pk, pk_val, error))

        poly = coord_text.split(' ')

        point_str = ""
        for point in poly:
            if point:
                try:
                    longitude, lattitude, other = point.split(',')
                except Exception as error:
                    raise Exception("%s %s: Error splitting 'text': %s" % (pk, pk_val, error))
                point_str += "%s %s," % (longitude, lattitude)

        p = GEOSGeometry('POLYGON((%s))' % point_str.strip()[:-1])
        neighborhood.area = p

        if existing:
            self.stats['existing'] += 1
        else:
            self.stats['new'] += 1

        return neighborhood
