# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Friendship'
        db.create_table(u'friends_friendship', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_friend', self.gf('django.db.models.fields.related.ForeignKey')(related_name='friend_set', to=orm['users.BookmarksUser'])),
            ('to_friend', self.gf('django.db.models.fields.related.ForeignKey')(related_name='to_friend_set', to=orm['users.BookmarksUser'])),
        ))
        db.send_create_signal(u'friends', ['Friendship'])

        # Adding unique constraint on 'Friendship', fields ['to_friend', 'from_friend']
        db.create_unique(u'friends_friendship', ['to_friend_id', 'from_friend_id'])

        # Adding model 'Invitation'
        db.create_table(u'friends_invitation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.BookmarksUser'])),
        ))
        db.send_create_signal(u'friends', ['Invitation'])


    def backwards(self, orm):
        # Removing unique constraint on 'Friendship', fields ['to_friend', 'from_friend']
        db.delete_unique(u'friends_friendship', ['to_friend_id', 'from_friend_id'])

        # Deleting model 'Friendship'
        db.delete_table(u'friends_friendship')

        # Deleting model 'Invitation'
        db.delete_table(u'friends_invitation')


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
        u'friends.friendship': {
            'Meta': {'unique_together': "(('to_friend', 'from_friend'),)", 'object_name': 'Friendship'},
            'from_friend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'friend_set'", 'to': u"orm['users.BookmarksUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'to_friend': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to_friend_set'", 'to': u"orm['users.BookmarksUser']"})
        },
        u'friends.invitation': {
            'Meta': {'object_name': 'Invitation'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.BookmarksUser']"})
        },
        u'users.bookmarksuser': {
            'Meta': {'object_name': 'BookmarksUser'},
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'key_expires': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['friends']