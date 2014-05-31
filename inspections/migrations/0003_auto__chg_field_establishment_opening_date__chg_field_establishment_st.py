# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Establishment.opening_date'
        db.alter_column('inspections_establishment', 'opening_date', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Establishment.state_id'
        db.alter_column('inspections_establishment', 'state_id', self.gf('django.db.models.fields.BigIntegerField')(null=True))

    def backwards(self, orm):

        # Changing field 'Establishment.opening_date'
        db.alter_column('inspections_establishment', 'opening_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1970, 1, 1, 0, 0)))

        # Changing field 'Establishment.state_id'
        db.alter_column('inspections_establishment', 'state_id', self.gf('django.db.models.fields.BigIntegerField')(default=0))

    models = {
        'inspections.establishment': {
            'Meta': {'unique_together': "(('external_id', 'county'),)", 'object_name': 'Establishment'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'county': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'opening_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '64'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'property_id': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '128'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'state_id': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True', 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '32'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'})
        },
        'inspections.inspection': {
            'Meta': {'object_name': 'Inspection'},
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'establishment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inspections'", 'to': "orm['inspections.Establishment']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.FloatField', [], {'blank': 'True', 'null': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'})
        },
        'inspections.violation': {
            'Meta': {'object_name': 'Violation'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'establishment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'violations'", 'to': "orm['inspections.Establishment']"}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'violations'", 'blank': 'True', 'to': "orm['inspections.Inspection']", 'null': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['inspections']
