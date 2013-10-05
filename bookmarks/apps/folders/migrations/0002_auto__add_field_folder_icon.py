# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Folder.icon'
        db.add_column(u'folders_folder', 'icon',
                      self.gf('django.db.models.fields.CharField')(default='default', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Folder.icon'
        db.delete_column(u'folders_folder', 'icon')


    models = {
        u'folders.folder': {
            'Meta': {'object_name': 'Folder'},
            'icon': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '20'}),
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