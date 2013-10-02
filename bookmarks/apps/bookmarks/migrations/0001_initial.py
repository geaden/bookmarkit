# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Link'
        db.create_table(u'bookmarks_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'bookmarks', ['Link'])

        # Adding model 'Bookmark'
        db.create_table(u'bookmarks_bookmark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.BookmarksUser'])),
            ('link', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.Link'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('folder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['folders.Folder'], null=True, blank=True)),
        ))
        db.send_create_signal(u'bookmarks', ['Bookmark'])

        # Adding model 'SharedBookmark'
        db.create_table(u'bookmarks_sharedbookmark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bookmark', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bookmarks.Bookmark'], unique=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('votes', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'bookmarks', ['SharedBookmark'])

        # Adding M2M table for field user_voted on 'SharedBookmark'
        db.create_table(u'bookmarks_sharedbookmark_user_voted', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sharedbookmark', models.ForeignKey(orm[u'bookmarks.sharedbookmark'], null=False)),
            ('bookmarksuser', models.ForeignKey(orm[u'users.bookmarksuser'], null=False))
        ))
        db.create_unique(u'bookmarks_sharedbookmark_user_voted', ['sharedbookmark_id', 'bookmarksuser_id'])


    def backwards(self, orm):
        # Deleting model 'Link'
        db.delete_table(u'bookmarks_link')

        # Deleting model 'Bookmark'
        db.delete_table(u'bookmarks_bookmark')

        # Deleting model 'SharedBookmark'
        db.delete_table(u'bookmarks_sharedbookmark')

        # Removing M2M table for field user_voted on 'SharedBookmark'
        db.delete_table('bookmarks_sharedbookmark_user_voted')


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
        u'bookmarks.bookmark': {
            'Meta': {'object_name': 'Bookmark'},
            'folder': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['folders.Folder']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.Link']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.BookmarksUser']"})
        },
        u'bookmarks.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'bookmarks.sharedbookmark': {
            'Meta': {'object_name': 'SharedBookmark'},
            'bookmark': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bookmarks.Bookmark']", 'unique': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user_voted': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['users.BookmarksUser']", 'symmetrical': 'False'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'folders.folder': {
            'Meta': {'object_name': 'Folder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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

    complete_apps = ['bookmarks']