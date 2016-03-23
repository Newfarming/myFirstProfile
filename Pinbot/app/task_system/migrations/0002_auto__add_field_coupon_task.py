# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Coupon.task'
        db.add_column(u'task_system_coupon', 'task',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='coupon_task', to=orm['task_system.Task']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Coupon.task'
        db.delete_column(u'task_system_coupon', 'task_id')


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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'task_system.coupon': {
            'Meta': {'object_name': 'Coupon'},
            'coupon_due_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 1, 15, 0, 0)'}),
            'coupon_num': ('django.db.models.fields.FloatField', [], {}),
            'coupon_start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'coupon_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'coupon_used_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coupon_task'", 'to': u"orm['task_system.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coupon_user'", 'to': u"orm['auth.User']"})
        },
        u'task_system.realreward': {
            'Meta': {'object_name': 'RealReward'},
            'award_item': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'award_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reward_user'", 'to': u"orm['auth.User']"})
        },
        u'task_system.task': {
            'Meta': {'object_name': 'Task'},
            'coupon_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reward_due_time': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'reward_num': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'reward_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'task_code': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'task_count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'task_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'task_level': ('django.db.models.fields.IntegerField', [], {}),
            'task_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'task_reward': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'task_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'task_url': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'weixin_required': ('django.db.models.fields.BooleanField', [], {})
        },
        u'task_system.taskfinishednotify': {
            'Meta': {'object_name': 'TaskFinishedNotify'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notify_status': ('django.db.models.fields.CharField', [], {'default': "'task_to_do'", 'max_length': '25'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notify_user'", 'to': u"orm['auth.User']"})
        },
        u'task_system.taskfinishedstatus': {
            'Meta': {'object_name': 'TaskFinishedStatus'},
            'current_process': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'finished_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'finished_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reward_due_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'reward_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'reward_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taskname'", 'to': u"orm['task_system.Task']"}),
            'task_times': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'task_finished_user'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['task_system']