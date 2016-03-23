# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Feed'
        db.create_table('feed_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_obj_id', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('keywords', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('job_type', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('talent_level', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('expect_area', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('job_desc', self.gf('django.db.models.fields.CharField')(default='', max_length=5000)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delete_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 5, 0, 0))),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('expire_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('ignored', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_click_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 5, 0, 0), auto_now_add=True, blank=True)),
            ('feed_expire_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 13, 0, 0))),
        ))
        db.send_create_signal('feed', ['Feed'])

        # Adding model 'FeedRemark'
        db.create_table(u'feed_feedremark', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feed.Feed'])),
            ('keywords_type', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('add_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'feed', ['FeedRemark'])

        # Adding model 'UserReadResume'
        db.create_table(u'feed_userreadresume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('source_type', self.gf('django.db.models.fields.IntegerField')(default=1, null=True, blank=True)),
            ('feed_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('resume_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('access_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'feed', ['UserReadResume'])

        # Adding model 'UserFeed'
        db.create_table(u'feed_userfeed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feed.Feed'])),
            ('user_charge_pkg', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transaction.UserChargePackage'], null=True, blank=True)),
            ('is_deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delete_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2015, 1, 5, 0, 0))),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('expire_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'feed', ['UserFeed'])

        # Adding model 'ReceiveResume'
        db.create_table(u'feed_receiveresume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receive_resume', to=orm['auth.User'])),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['my_resume.Resume'])),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['feed.Feed'])),
            ('feed_status', self.gf('django.db.models.fields.CharField')(default='waiting', max_length=20)),
            ('send_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('send_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='send_resume', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'feed', ['ReceiveResume'])


    def backwards(self, orm):
        # Deleting model 'Feed'
        db.delete_table('feed_feed')

        # Deleting model 'FeedRemark'
        db.delete_table(u'feed_feedremark')

        # Deleting model 'UserReadResume'
        db.delete_table(u'feed_userreadresume')

        # Deleting model 'UserFeed'
        db.delete_table(u'feed_userfeed')

        # Deleting model 'ReceiveResume'
        db.delete_table(u'feed_receiveresume')


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
        'feed.feed': {
            'Meta': {'object_name': 'Feed'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {}),
            'delete_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'expect_area': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'expire_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feed_expire_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 13, 0, 0)'}),
            'feed_obj_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5000'}),
            'job_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'last_click_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'talent_level': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        },
        u'feed.feedremark': {
            'Meta': {'object_name': 'FeedRemark'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {}),
            'add_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'keywords_type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'feed.receiveresume': {
            'Meta': {'object_name': 'ReceiveResume'},
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Feed']"}),
            'feed_status': ('django.db.models.fields.CharField', [], {'default': "'waiting'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['my_resume.Resume']"}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'send_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'send_resume'", 'to': u"orm['auth.User']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receive_resume'", 'to': u"orm['auth.User']"})
        },
        u'feed.userfeed': {
            'Meta': {'object_name': 'UserFeed'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {}),
            'delete_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)'}),
            'expire_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'user_charge_pkg': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transaction.UserChargePackage']", 'null': 'True', 'blank': 'True'})
        },
        u'feed.userreadresume': {
            'Meta': {'object_name': 'UserReadResume'},
            'access_time': ('django.db.models.fields.DateTimeField', [], {}),
            'feed_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resume_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'source_type': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'my_resume.resume': {
            'Meta': {'object_name': 'Resume'},
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avatar_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'birthday': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1980, 1, 1, 0, 0)'}),
            'certificate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_salary': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'degree': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
            'hobbies': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'homepage': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'job_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['system.PositionCategory']", 'null': 'True', 'blank': 'True'}),
            'job_hunting_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'language_skills': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'major': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'other_info': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'perf_at_school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'political_landscape': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'qq': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'research_perf': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'residence': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'resume_id': ('django.db.models.fields.CharField', [], {'default': "'54aa62268230db3d2c92fdc9'", 'max_length': '50'}),
            'school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'self_evaluation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400'}),
            'target_salary': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'work_years': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'payment.paymentorder': {
            'Meta': {'object_name': 'PaymentOrder'},
            'actual_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'feed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feed_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'feed_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.FeedService']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.ResumePackge']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'package_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'pay_status': ('django.db.models.fields.CharField', [], {'default': "'unpay'", 'max_length': '20'}),
            'payment_terms': ('django.db.models.fields.CharField', [], {'default': "'alipay'", 'max_length': '20'}),
            'total_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'pinbot_package.feedservice': {
            'Meta': {'object_name': 'FeedService'},
            'display': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feed_num': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'pinbot_package.resumepackge': {
            'Meta': {'object_name': 'ResumePackge'},
            'actual_resume_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'company_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'display': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feed_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.FeedService']"}),
            'feed_service_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feed_service_value': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'resume_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'total_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'valid_days': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'system.positioncategory': {
            'Meta': {'object_name': 'PositionCategory'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'transaction.userchargepackage': {
            'Meta': {'object_name': 'UserChargePackage'},
            'actual_cost': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'extra_feed_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feed_end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 1, 5, 0, 0)'}),
            'feed_package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.FeedService']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['payment.PaymentOrder']", 'null': 'True', 'blank': 'True'}),
            'package_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pay_status': ('django.db.models.fields.CharField', [], {'default': "'Start'", 'max_length': '50'}),
            're_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rest_feed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rest_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'resume_end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2016, 1, 5, 0, 0)'}),
            'resume_package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.ResumePackge']", 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 1, 5, 0, 0)'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'zero_points_notify_status': ('django.db.models.fields.CharField', [], {'default': "'read'", 'max_length': '50'})
        }
    }

    complete_apps = ['feed']