# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SendCompanyCard.feed_id'
        db.alter_column(u'jobs_sendcompanycard', 'feed_id', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))
        # Deleting field 'Company.category'
        db.delete_column(u'jobs_company', 'category_id')

        # Adding M2M table for field category on 'Company'
        m2m_table_name = db.shorten_name(u'jobs_company_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('company', models.ForeignKey(orm[u'jobs.company'], null=False)),
            ('companycategory', models.ForeignKey(orm[u'jobs.companycategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['company_id', 'companycategory_id'])

        # Adding field 'CompanyCategory.brick_display'
        db.add_column(u'jobs_companycategory', 'brick_display',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):

        # Changing field 'SendCompanyCard.feed_id'
        db.alter_column(u'jobs_sendcompanycard', 'feed_id', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Adding field 'Company.category'
        db.add_column(u'jobs_company', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['jobs.CompanyCategory'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Removing M2M table for field category on 'Company'
        db.delete_table(db.shorten_name(u'jobs_company_category'))

        # Deleting field 'CompanyCategory.brick_display'
        db.delete_column(u'jobs_companycategory', 'brick_display')


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
        u'jobs.company': {
            'Meta': {'object_name': 'Company'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 10, 0, 0)'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['jobs.CompanyCategory']", 'null': 'True', 'blank': 'True'}),
            'company_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'company_stage': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'core_team': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'favour_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_points': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'pinbot_recommend': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'product_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'jobs.companycategory': {
            'Meta': {'object_name': 'CompanyCategory'},
            'brick_display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'jobs.hunterinterest': {
            'Meta': {'object_name': 'HunterInterest'},
            'access_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 10, 0, 0)'}),
            'click': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Company']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interest_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'ip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'is_interest': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Job']", 'null': 'True', 'blank': 'True'}),
            'refer_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'})
        },
        u'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 10, 0, 0)'}),
            'address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Company']"}),
            'degree': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_points': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'salary_high': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'salary_low': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'skill_desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'work_years': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'jobs.sendcompanycard': {
            'Meta': {'object_name': 'SendCompanyCard'},
            'download_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'feed_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'feedback_status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'feedback_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 10, 0, 0)'}),
            'has_download': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Job']", 'null': 'True', 'blank': 'True'}),
            'points_used': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'resume_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'send_msg': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'send_status': ('django.db.models.fields.IntegerField', [], {'default': '2', 'null': 'True', 'blank': 'True'}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 3, 10, 0, 0)'}),
            'send_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'to_email': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'jobs.userfavourcompany': {
            'Meta': {'object_name': 'UserFavourCompany'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_favours'", 'to': u"orm['jobs.Company']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'favour_companys'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['jobs']