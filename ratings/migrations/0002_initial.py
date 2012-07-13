# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Business'
        db.create_table('ratings_business', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2)),
        ))
        db.send_create_signal('ratings', ['Business'])

        # Adding model 'UserFavorite'
        db.create_table('ratings_userfavorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Business'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ratings', ['UserFavorite'])

        # Adding model 'FacebookUser'
        db.create_table('ratings_facebookuser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fbuser_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('ratings', ['FacebookUser'])

        # Adding model 'PageRelationship'
        db.create_table('ratings_pagerelationship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wiki.Page'])),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Business'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Tag'])),
        ))
        db.send_create_signal('ratings', ['PageRelationship'])

        # Adding model 'Rating'
        db.create_table('ratings_rating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Business'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ratings', ['Rating'])

        # Adding model 'Comment'
        db.create_table('ratings_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reply_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='replies', null=True, to=orm['ratings.Comment'])),
            ('descr', self.gf('django.db.models.fields.TextField')(max_length=2000)),
        ))
        db.send_create_signal('ratings', ['Comment'])

        # Adding model 'TagComment'
        db.create_table('ratings_tagcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Comment'])),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tags.Tag'])),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Business'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ratings', ['TagComment'])

        # Adding model 'BusinessComment'
        db.create_table('ratings_businesscomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Business'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Comment'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('ratings', ['BusinessComment'])

        # Adding model 'CommentRating'
        db.create_table('ratings_commentrating', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ratings.Comment'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal('ratings', ['CommentRating'])


    def backwards(self, orm):
        # Deleting model 'Business'
        db.delete_table('ratings_business')

        # Deleting model 'UserFavorite'
        db.delete_table('ratings_userfavorite')

        # Deleting model 'FacebookUser'
        db.delete_table('ratings_facebookuser')

        # Deleting model 'PageRelationship'
        db.delete_table('ratings_pagerelationship')

        # Deleting model 'Rating'
        db.delete_table('ratings_rating')

        # Deleting model 'Comment'
        db.delete_table('ratings_comment')

        # Deleting model 'TagComment'
        db.delete_table('ratings_tagcomment')

        # Deleting model 'BusinessComment'
        db.delete_table('ratings_businesscomment')

        # Deleting model 'CommentRating'
        db.delete_table('ratings_commentrating')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'ratings.business': {
            'Meta': {'object_name': 'Business'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'})
        },
        'ratings.businesscomment': {
            'Meta': {'object_name': 'BusinessComment'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings.Business']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings.Comment']"})
        },
        'ratings.comment': {
            'Meta': {'object_name': 'Comment'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'descr': ('django.db.models.fields.TextField', [], {'max_length': '2000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reply_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'replies'", 'null': 'True', 'to': "orm['ratings.Comment']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ratings.commentrating': {
            'Meta': {'object_name': 'CommentRating'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings.Comment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ratings.facebookuser': {
            'Meta': {'object_name': 'FacebookUser'},
            'fbuser_id': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ratings.pagerelationship': {
            'Meta': {'object_name': 'PageRelationship'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings.Business']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wiki.Page']"}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Tag']"})
        },
        'ratings.rating': {
            'Meta': {'object_name': 'Rating'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings.Business']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'ratings.tagcomment': {
            'Meta': {'object_name': 'TagComment'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings.Business']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tags.Tag']"}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings.Comment']"})
        },
        'ratings.userfavorite': {
            'Meta': {'object_name': 'UserFavorite'},
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ratings.Business']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'tags.tag': {
            'Meta': {'object_name': 'Tag'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'descr': ('django.db.models.fields.TextField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'wiki.page': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rendered': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['ratings']