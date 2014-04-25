# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Establishment'
        db.create_table('inspections_establishment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('state_id', self.gf('django.db.models.fields.BigIntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('county', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(blank=True, max_length=64)),
            ('opening_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True, null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='active', max_length=32)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(blank=True, null=True)),
        ))
        db.send_create_signal('inspections', ['Establishment'])

        # Adding unique constraint on 'Establishment', fields ['external_id', 'county']
        db.create_unique('inspections_establishment', ['external_id', 'county'])

        # Adding model 'Inspection'
        db.create_table('inspections_inspection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('establishment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inspections', to=orm['inspections.Establishment'])),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('score', self.gf('django.db.models.fields.FloatField')(blank=True, null=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True, null=True)),
        ))
        db.send_create_signal('inspections', ['Inspection'])

        # Adding model 'Violation'
        db.create_table('inspections_violation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('establishment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='violations', to=orm['inspections.Establishment'])),
            ('inspection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='violations', to=orm['inspections.Inspection'], blank=True, null=True)),
            ('external_id', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(blank=True, db_index=True, null=True)),
        ))
        db.send_create_signal('inspections', ['Violation'])


    def backwards(self, orm):
        # Removing unique constraint on 'Establishment', fields ['external_id', 'county']
        db.delete_unique('inspections_establishment', ['external_id', 'county'])

        # Deleting model 'Establishment'
        db.delete_table('inspections_establishment')

        # Deleting model 'Inspection'
        db.delete_table('inspections_inspection')

        # Deleting model 'Violation'
        db.delete_table('inspections_violation')


    models = {
        'inspections.establishment': {
            'Meta': {'object_name': 'Establishment', 'unique_together': "(('external_id', 'county'),)"},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'county': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'blank': 'True', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'opening_date': ('django.db.models.fields.DateTimeField', [], {}),
            'phone_number': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '64'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'state_id': ('django.db.models.fields.BigIntegerField', [], {}),
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
            'inspection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'violations'", 'to': "orm['inspections.Inspection']", 'blank': 'True', 'null': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'db_index': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['inspections']