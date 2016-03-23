# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SmsCodeSendLog'
        db.delete_table(u'users_smscodesendlog')


        # Changing field 'UserProfile.phone'
        db.alter_column('users_userprofile', 'phone', self.gf('django.db.models.fields.CharField')(default='', max_length=50))

    def backwards(self, orm):
        # Adding model 'SmsCodeSendLog'
        db.create_table(u'users_smscodesendlog', (
            ('mobile', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('last_time', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('action_name', self.gf('django.db.models.fields.CharField')(default='Other', max_length=50)),
        ))
        db.send_create_signal(u'users', ['SmsCodeSendLog'])


        # Changing field 'UserProfile.phone'
        db.alter_column('users_userprofile', 'phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

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
        u'users.staffcustomerassgin': {
            'Meta': {'object_name': 'StaffCustomerAssgin', 'db_table': "'report_staffcustomerassgin'"},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 11, 6, 0, 0)'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stafftaskassign_customers'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stafftaskassign_operator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stafftaskassign_staffs'", 'to': u"orm['auth.User']"})
        },
        u'users.usercontactinfo': {
            'Meta': {'object_name': 'UserContactInfo'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contact_infos'", 'to': u"orm['auth.User']"}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        },
        u'users.usermailbox': {
            'Meta': {'object_name': 'UserMailbox'},
            'addTime': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'firstTime': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'lastSyncTime': ('django.db.models.fields.DateField', [], {}),
            'latestMailTotal': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'latestResumeNum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'latestSendTime': ('django.db.models.fields.DateField', [], {}),
            'mailType': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'port': ('django.db.models.fields.IntegerField', [], {}),
            'serverAddr': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'totalMailNum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'totalResumeNum': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uploadPath': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'activation_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'calc_level': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'client_level': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'company_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'guide_switch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'is_email_bind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_phone_bind': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_review': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'login_days': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'postcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'service_level': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'street': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'trans_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['users']