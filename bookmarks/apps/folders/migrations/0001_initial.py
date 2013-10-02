# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Folder'
        db.create_table(u'folders_folder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'folders', ['Folder'])

        # Adding model 'FolderSystem'
        db.create_table(u'folders_foldersystem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_folder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='children', to=orm['folders.Folder'])),
            ('child_folder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='parents', to=orm['folders.Folder'])),
        ))
        db.send_create_signal(u'folders', ['FolderSystem'])


    def backwards(self, orm):
        # Deleting model 'Folder'
        db.delete_table(u'folders_folder')

        # Deleting model 'FolderSystem'
        db.delete_table(u'folders_foldersystem')


    models = {
        u'folders.folder': {
            'Meta': {'object_name': 'Folder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'folders.foldersystem': {
            'Meta': {'object_name': 'FolderSystem'},
            'child_folder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'parents'", 'to': u"orm['folders.Folder']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_folder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'children'", 'to': u"orm['folders.Folder']"})
        }
    }

    complete_apps = ['folders']