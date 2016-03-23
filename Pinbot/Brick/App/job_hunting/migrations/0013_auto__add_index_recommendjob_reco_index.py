# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'RecommendJob', fields ['reco_index']
        db.create_index(u'job_hunting_recommendjob', ['reco_index'])


    def backwards(self, orm):
        # Removing index on 'RecommendJob', fields ['reco_index']
        db.delete_index(u'job_hunting_recommendjob', ['reco_index'])


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
            'category': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['jobs.Company']", 'null': 'True', 'blank': 'True'}),
            'degree': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'delete_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 2, 4, 0, 0)'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'department_to': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'expect_area': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'expire_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'feed_expire_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 2, 12, 0, 0)'}),
            'feed_obj_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'feed_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '5000'}),
            'job_tag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'job_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'job_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'key_points': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'keywords': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'last_click_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 2, 4, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'recruit_num': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'report_to': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'salary_max': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'salary_min': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'skill_required': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000'}),
            'talent_level': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'username': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'work_years_max': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'work_years_min': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'job_hunting.companycardjob': {
            'Meta': {'unique_together': "(('hr_user', 'user', 'job'),)", 'object_name': 'CompanyCardJob'},
            'action_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hr_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'send_card_jobs'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'send_jobs'", 'to': u"orm['jobs.Job']"}),
            'send_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'waiting'", 'max_length': '30'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '70'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'card_jobs'", 'to': u"orm['auth.User']"})
        },
        u'job_hunting.jobmessage': {
            'Meta': {'object_name': 'JobMessage'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['job_hunting.JobMessage']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'job_hunting.recommendconf': {
            'Meta': {'object_name': 'RecommendConf'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'job_hunting.recommendjob': {
            'Meta': {'unique_together': "(('search_tag', 'hr_user', 'user', 'job'),)", 'object_name': 'RecommendJob'},
            'action': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'action_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'company_action': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'company_action_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'company_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'hr_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'receive_jobs'", 'null': 'True', 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['feed.Feed']"}),
            'read_status': ('django.db.models.fields.CharField', [], {'default': "'unread'", 'max_length': '10'}),
            'reco_index': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_index': 'True'}),
            'reco_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['my_resume.Resume']"}),
            'search_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['my_resume.SearchTag']", 'null': 'True', 'blank': 'True'}),
            'succ_rate': ('django.db.models.fields.FloatField', [], {'default': '66.6'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recommend_jobs'", 'to': u"orm['auth.User']"})
        },
        u'jobs.company': {
            'Meta': {'object_name': 'Company'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 2, 4, 0, 0)'}),
            'company_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'company_stage': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'core_team': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key_points': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'pinbot_recommend': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'product_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'jobs.job': {
            'Meta': {'object_name': 'Job'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 2, 4, 0, 0)'}),
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
            'job_category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['system.PositionCategory']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
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
            'resume_id': ('django.db.models.fields.CharField', [], {'default': "'54d203f28230dbfedd669313'", 'max_length': '50'}),
            'school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'self_evaluation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400'}),
            'target_salary': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'work_years': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'my_resume.searchtag': {
            'Meta': {'object_name': 'SearchTag'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'citys': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'degree': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'search_tags'", 'to': u"orm['my_resume.Resume']"}),
            'tags': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'}),
            'work_years': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        u'system.positioncategory': {
            'Meta': {'object_name': 'PositionCategory'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['job_hunting']