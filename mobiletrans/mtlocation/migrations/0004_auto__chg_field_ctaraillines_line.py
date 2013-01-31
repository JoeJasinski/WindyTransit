# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'CTARailLines.line'
        db.alter_column(u'mtlocation_ctaraillines', 'line', self.gf('django.contrib.gis.db.models.fields.LineStringField')())


    def backwards(self, orm):
        
        # Changing field 'CTARailLines.line'
        db.alter_column(u'mtlocation_ctaraillines', 'line', self.gf('django.contrib.gis.db.models.fields.LineStringField')(srid=-1))


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'mtlocation.ctaraillines': {
            'Meta': {'object_name': 'CTARailLines'},
            'alt_legend': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'asset_id': ('django.db.models.fields.IntegerField', [], {}),
            'branch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legend': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'line': ('django.contrib.gis.db.models.fields.LineStringField', [], {}),
            'objectid': ('django.db.models.fields.IntegerField', [], {}),
            'segment_id': ('django.db.models.fields.IntegerField', [], {}),
            'shape_len': ('django.db.models.fields.FloatField', [], {}),
            'transit_lines': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.IntegerField', [], {})
        },
        u'mtlocation.gplace': {
            'Meta': {'object_name': 'GPlace', '_ormbases': [u'mtlocation.Location']},
            'address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'international_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'local_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            u'location_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mtlocation.Location']", 'unique': 'True', 'primary_key': 'True'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '2', 'blank': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'types': ('mobiletrans.mtlocation.fields.SeparatedValuesField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vicinity': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'mtlocation.hospital': {
            'Meta': {'object_name': 'Hospital', '_ormbases': [u'mtlocation.Location']},
            u'location_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mtlocation.Location']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'mtlocation.landmark': {
            'Meta': {'object_name': 'Landmark', '_ormbases': [u'mtlocation.Location']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'architect': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'build_date': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'landmark_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'location_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mtlocation.Location']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'mtlocation.library': {
            'Meta': {'object_name': 'Library', '_ormbases': [u'mtlocation.Location']},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hours': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'location_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mtlocation.Location']", 'unique': 'True', 'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'mtlocation.location': {
            'Meta': {'object_name': 'Location'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '255', 'populate_from': 'None', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'mtlocation.neighborhood': {
            'Meta': {'object_name': 'Neighborhood', '_ormbases': [u'mtlocation.Region']},
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'region_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mtlocation.Region']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'mtlocation.region': {
            'Meta': {'object_name': 'Region'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'area': ('django.contrib.gis.db.models.fields.PolygonField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '255', 'populate_from': 'None', 'db_index': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'mtlocation.transitroute': {
            'Meta': {'object_name': 'TransitRoute'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'route_id': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'text_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'})
        },
        u'mtlocation.transitstop': {
            'Meta': {'object_name': 'TransitStop', '_ormbases': [u'mtlocation.Location']},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'location_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mtlocation.Location']", 'unique': 'True', 'primary_key': 'True'}),
            'location_type': ('django.db.models.fields.IntegerField', [], {}),
            'route': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['mtlocation.TransitRoute']", 'null': 'True', 'blank': 'True'}),
            'stop_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stop_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'mtlocation.zipcode': {
            'Meta': {'object_name': 'Zipcode', '_ormbases': [u'mtlocation.Region']},
            u'region_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mtlocation.Region']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['mtlocation']
