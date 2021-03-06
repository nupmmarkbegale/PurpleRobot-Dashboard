# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DashboardUser.last_name'
        db.delete_column(u'users_dashboarduser', 'last_name')

        # Deleting field 'DashboardUser.date_joined'
        db.delete_column(u'users_dashboarduser', 'date_joined')

        # Deleting field 'DashboardUser.first_name'
        db.delete_column(u'users_dashboarduser', 'first_name')

        # Adding field 'DashboardUser.joined'
        db.add_column(u'users_dashboarduser', 'joined',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 5, 9, 0, 0), blank=True),
                      keep_default=False)

        # Adding index on 'DashboardUser', fields ['username']
        db.create_index(u'users_dashboarduser', ['username'])


        # Changing field 'DashboardUser.email'
        db.alter_column(u'users_dashboarduser', 'email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=254))
        # Adding unique constraint on 'DashboardUser', fields ['email']
        db.create_unique(u'users_dashboarduser', ['email'])


    def backwards(self, orm):
        # Removing unique constraint on 'DashboardUser', fields ['email']
        db.delete_unique(u'users_dashboarduser', ['email'])

        # Removing index on 'DashboardUser', fields ['username']
        db.delete_index(u'users_dashboarduser', ['username'])

        # Adding field 'DashboardUser.last_name'
        db.add_column(u'users_dashboarduser', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Adding field 'DashboardUser.date_joined'
        db.add_column(u'users_dashboarduser', 'date_joined',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'DashboardUser.first_name'
        db.add_column(u'users_dashboarduser', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True),
                      keep_default=False)

        # Deleting field 'DashboardUser.joined'
        db.delete_column(u'users_dashboarduser', 'joined')


        # Changing field 'DashboardUser.email'
        db.alter_column(u'users_dashboarduser', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.dashboarduser': {
            'Meta': {'object_name': 'DashboardUser'},
            'affiliation': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'})
        }
    }

    complete_apps = ['users']