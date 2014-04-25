# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Establishment.property_id'
        db.add_column('inspections_establishment', 'property_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Establishment.property_id'
        db.delete_column('inspections_establishment', 'property_id')


    models = {
        'inspections.establishment': {
            'Meta': {'unique_together': "(('external_id', 'county'),)", 'object_name': 'Establishment'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'county': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'opening_date': ('django.db.models.fields.DateTimeField', [], {}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'property_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'state_id': ('django.db.models.fields.BigIntegerField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '32'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'})
        },
        'inspections.inspection': {
            'Meta': {'object_name': 'Inspection'},
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'establishment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inspections'", 'to': "orm['inspections.Establishment']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'})
        },
        'inspections.violation': {
            'Meta': {'object_name': 'Violation'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'establishment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'violations'", 'to': "orm['inspections.Establishment']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'null': 'True', 'related_name': "'violations'", 'to': "orm['inspections.Inspection']"}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['inspections']