# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ShoppingCar'
        db.create_table(u'payment_shoppingcar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pinbot_package.ResumePackge'], null=True, on_delete=models.PROTECT, blank=True)),
            ('package_price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('feed_service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pinbot_package.FeedService'], null=True, on_delete=models.PROTECT, blank=True)),
            ('feed_price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('feed_count', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('total_price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'payment', ['ShoppingCar'])

        # Adding model 'PaymentOrder'
        db.create_table(u'payment_paymentorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pinbot_package.ResumePackge'], null=True, on_delete=models.PROTECT, blank=True)),
            ('package_price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('feed_service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pinbot_package.FeedService'], null=True, on_delete=models.PROTECT, blank=True)),
            ('feed_price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('feed_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('pay_status', self.gf('django.db.models.fields.CharField')(default='unpay', max_length=20)),
            ('total_price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('actual_price', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('payment_terms', self.gf('django.db.models.fields.CharField')(default='alipay', max_length=20)),
        ))
        db.send_create_signal(u'payment', ['PaymentOrder'])

        # Adding model 'ReceiverInfo'
        db.create_table(u'payment_receiverinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('default_addr', self.gf('django.db.models.fields.CharField')(default='no', max_length=10)),
        ))
        db.send_create_signal(u'payment', ['ReceiverInfo'])

        # Adding model 'BillInfo'
        db.create_table(u'payment_billinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('bill_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'payment', ['BillInfo'])

        # Adding model 'OrderBillInfo'
        db.create_table(u'payment_orderbillinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('bill_type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('order', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['payment.PaymentOrder'], unique=True)),
        ))
        db.send_create_signal(u'payment', ['OrderBillInfo'])

        # Adding model 'OrderReceiverInfo'
        db.create_table(u'payment_orderreceiverinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40, db_index=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, db_index=True)),
            ('order', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['payment.PaymentOrder'], unique=True)),
        ))
        db.send_create_signal(u'payment', ['OrderReceiverInfo'])


    def backwards(self, orm):
        # Deleting model 'ShoppingCar'
        db.delete_table(u'payment_shoppingcar')

        # Deleting model 'PaymentOrder'
        db.delete_table(u'payment_paymentorder')

        # Deleting model 'ReceiverInfo'
        db.delete_table(u'payment_receiverinfo')

        # Deleting model 'BillInfo'
        db.delete_table(u'payment_billinfo')

        # Deleting model 'OrderBillInfo'
        db.delete_table(u'payment_orderbillinfo')

        # Deleting model 'OrderReceiverInfo'
        db.delete_table(u'payment_orderreceiverinfo')


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
        u'payment.billinfo': {
            'Meta': {'object_name': 'BillInfo'},
            'bill_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'payment.orderbillinfo': {
            'Meta': {'object_name': 'OrderBillInfo'},
            'bill_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['payment.PaymentOrder']", 'unique': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'payment.orderreceiverinfo': {
            'Meta': {'object_name': 'OrderReceiverInfo'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'order': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['payment.PaymentOrder']", 'unique': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
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
        u'payment.receiverinfo': {
            'Meta': {'object_name': 'ReceiverInfo'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'default_addr': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'payment.shoppingcar': {
            'Meta': {'object_name': 'ShoppingCar'},
            'feed_count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'feed_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'feed_service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.FeedService']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pinbot_package.ResumePackge']", 'null': 'True', 'on_delete': 'models.PROTECT', 'blank': 'True'}),
            'package_price': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'total_price': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
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
        }
    }

    complete_apps = ['payment']