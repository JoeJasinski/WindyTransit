# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Location'
        db.create_table(u'mtlocation_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=255, populate_from=None, db_index=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal(u'mtlocation', ['Location'])

        # Adding model 'Landmark'
        db.create_table(u'mtlocation_landmark', (
            (u'location_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mtlocation.Location'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('architect', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('build_date', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('landmark_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'mtlocation', ['Landmark'])

        # Adding model 'TransitStop'
        db.create_table(u'mtlocation_transitstop', (
            (u'location_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mtlocation.Location'], unique=True, primary_key=True)),
            ('stop_id', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('stop_code', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('location_type', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'mtlocation', ['TransitStop'])

        # Adding M2M table for field route on 'TransitStop'
        db.create_table(u'mtlocation_transitstop_route', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('transitstop', models.ForeignKey(orm[u'mtlocation.transitstop'], null=False)),
            ('transitroute', models.ForeignKey(orm[u'mtlocation.transitroute'], null=False))
        ))
        db.create_unique(u'mtlocation_transitstop_route', ['transitstop_id', 'transitroute_id'])

        # Adding model 'TransitRoute'
        db.create_table(u'mtlocation_transitroute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('route_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')()),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('text_color', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'mtlocation', ['TransitRoute'])

        # Adding model 'Library'
        db.create_table(u'mtlocation_library', (
            (u'location_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mtlocation.Location'], unique=True, primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('hours', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'mtlocation', ['Library'])

        # Adding model 'Hospital'
        db.create_table(u'mtlocation_hospital', (
            (u'location_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mtlocation.Location'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'mtlocation', ['Hospital'])

        # Adding model 'Region'
        db.create_table(u'mtlocation_region', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('autoslug.fields.AutoSlugField')(unique_with=(), max_length=255, populate_from=None, db_index=True)),
            ('area', self.gf('django.contrib.gis.db.models.fields.PolygonField')()),
            ('uuid', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
        ))
        db.send_create_signal(u'mtlocation', ['Region'])

        # Adding model 'Neighborhood'
        db.create_table(u'mtlocation_neighborhood', (
            (u'region_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mtlocation.Region'], unique=True, primary_key=True)),
            ('long_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal(u'mtlocation', ['Neighborhood'])

        # Adding model 'Zipcode'
        db.create_table(u'mtlocation_zipcode', (
            (u'region_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mtlocation.Region'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'mtlocation', ['Zipcode'])

        # Adding model 'GPlace'
        db.create_table(u'mtlocation_gplace', (
            (u'location_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mtlocation.Location'], unique=True, primary_key=True)),
            ('rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=2, blank=True)),
            ('vicinity', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('types', self.gf('mobiletrans.mtlocation.fields.SeparatedValuesField')(null=True, blank=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('international_phone_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('local_phone_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'mtlocation', ['GPlace'])


    def backwards(self, orm):
        
        # Deleting model 'Location'
        db.delete_table(u'mtlocation_location')

        # Deleting model 'Landmark'
        db.delete_table(u'mtlocation_landmark')

        # Deleting model 'TransitStop'
        db.delete_table(u'mtlocation_transitstop')

        # Removing M2M table for field route on 'TransitStop'
        db.delete_table('mtlocation_transitstop_route')

        # Deleting model 'TransitRoute'
        db.delete_table(u'mtlocation_transitroute')

        # Deleting model 'Library'
        db.delete_table(u'mtlocation_library')

        # Deleting model 'Hospital'
        db.delete_table(u'mtlocation_hospital')

        # Deleting model 'Region'
        db.delete_table(u'mtlocation_region')

        # Deleting model 'Neighborhood'
        db.delete_table(u'mtlocation_neighborhood')

        # Deleting model 'Zipcode'
        db.delete_table(u'mtlocation_zipcode')

        # Deleting model 'GPlace'
        db.delete_table(u'mtlocation_gplace')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36'})
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
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
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
