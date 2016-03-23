# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('users_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('user_email', self.gf('django.db.models.fields.EmailField')(max_length=30)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('company_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('is_review', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('qq', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('street', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('province', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(default='', max_length=30, blank=True)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('guide_switch', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('role', self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True)),
        ))
        db.send_create_signal(u'users', ['UserProfile'])

        # Adding model 'UserMailbox'
        db.create_table(u'users_usermailbox', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('serverAddr', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('interval', self.gf('django.db.models.fields.IntegerField')(default=30)),
            ('port', self.gf('django.db.models.fields.IntegerField')()),
            ('mailType', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('addTime', self.gf('django.db.models.fields.DateField')()),
            ('lastSyncTime', self.gf('django.db.models.fields.DateField')()),
            ('latestSendTime', self.gf('django.db.models.fields.DateField')()),
            ('firstTime', self.gf('django.db.models.fields.BooleanField')()),
            ('latestMailTotal', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('latestResumeNum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('totalResumeNum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('totalMailNum', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('uploadPath', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'users', ['UserMailbox'])

        # Adding model 'StaffCustomerAssgin'
        db.create_table('report_staffcustomerassgin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stafftaskassign_customers', to=orm['auth.User'])),
            ('staff', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stafftaskassign_staffs', to=orm['auth.User'])),
            ('operator', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='stafftaskassign_operator', null=True, to=orm['auth.User'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 28, 0, 0))),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'users', ['StaffCustomerAssgin'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('users_userprofile')

        # Deleting model 'UserMailbox'
        db.delete_table(u'users_usermailbox')

        # Deleting model 'StaffCustomerAssgin'
        db.delete_table('report_staffcustomerassgin')


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
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 28, 0, 0)'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stafftaskassign_customers'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stafftaskassign_operator'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'staff': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stafftaskassign_staffs'", 'to': u"orm['auth.User']"})
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
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'company_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'guide_switch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'is_review': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'province': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30', 'blank': 'True'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'street': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['users']