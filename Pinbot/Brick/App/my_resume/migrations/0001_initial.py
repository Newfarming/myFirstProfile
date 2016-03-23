# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Resume'
        db.create_table(u'my_resume_resume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('current_salary', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('job_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.PositionCategory'], null=True, blank=True)),
            ('job_hunting_state', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('target_salary', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('certificate', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('qq', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('avatar_url', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('email', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('age', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('school', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('degree', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('marital_status', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('major', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('address', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('residence', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('work_years', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('birthday', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(1980, 1, 1, 0, 0))),
            ('political_landscape', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('identity_id', self.gf('django.db.models.fields.CharField')(default='', max_length=25)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='', max_length=15)),
            ('homepage', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('other_info', self.gf('django.db.models.fields.TextField')(default='')),
            ('research_perf', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('hobbies', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('language_skills', self.gf('django.db.models.fields.CharField')(default='', max_length=100)),
            ('perf_at_school', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('self_evaluation', self.gf('django.db.models.fields.CharField')(default='', max_length=400)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('resume_id', self.gf('django.db.models.fields.CharField')(default='54b8b4778230db3885bc2cb1', max_length=50)),
        ))
        db.send_create_signal(u'my_resume', ['Resume'])

        # Adding model 'ResumePositionTag'
        db.create_table(u'my_resume_resumepositiontag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(related_name='position_tags', to=orm['my_resume.Resume'])),
            ('position_tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.PositionCategoryTag'])),
        ))
        db.send_create_signal(u'my_resume', ['ResumePositionTag'])

        # Adding model 'ResumeTargetCity'
        db.create_table(u'my_resume_resumetargetcity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(related_name='expectation_area', to=orm['my_resume.Resume'])),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['system.City'])),
        ))
        db.send_create_signal(u'my_resume', ['ResumeTargetCity'])

        # Adding model 'WorkExperience'
        db.create_table(u'my_resume_workexperience', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(related_name='works', to=orm['my_resume.Resume'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('position_title', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('duration', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('min_salary', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('max_salary', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('company_category', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('industry_category', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('company_name', self.gf('django.db.models.fields.CharField')(default='', max_length=40)),
            ('job_desc', self.gf('django.db.models.fields.TextField')(default='')),
            ('position_category', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
        ))
        db.send_create_signal(u'my_resume', ['WorkExperience'])

        # Adding model 'Project'
        db.create_table(u'my_resume_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(related_name='projects', to=orm['my_resume.Resume'])),
            ('project_desc', self.gf('django.db.models.fields.CharField')(default='', max_length=500)),
            ('project_name', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('job_title', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('responsible_for', self.gf('django.db.models.fields.CharField')(default='', max_length=300)),
            ('company_name', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
        ))
        db.send_create_signal(u'my_resume', ['Project'])

        # Adding model 'Education'
        db.create_table(u'my_resume_education', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(related_name='educations', to=orm['my_resume.Resume'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('school', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('degree', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('major', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
        ))
        db.send_create_signal(u'my_resume', ['Education'])

        # Adding model 'Training'
        db.create_table(u'my_resume_training', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trainings', to=orm['my_resume.Resume'])),
            ('certificate', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('course', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('instituation', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=60)),
            ('train_desc', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
        ))
        db.send_create_signal(u'my_resume', ['Training'])

        # Adding model 'ProfessionalSkill'
        db.create_table(u'my_resume_professionalskill', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume', self.gf('django.db.models.fields.related.ForeignKey')(related_name='professional_skills', to=orm['my_resume.Resume'])),
            ('skill_desc', self.gf('django.db.models.fields.CharField')(default='', max_length=30)),
            ('proficiency', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('month', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'my_resume', ['ProfessionalSkill'])

        # Adding model 'SocialPage'
        db.create_table(u'my_resume_socialpage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('resume', self.gf('django.db.models.fields.related.OneToOneField')(related_name='social_page', unique=True, to=orm['my_resume.Resume'])),
            ('twitter', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('weibo', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('zhihu', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('github', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
            ('dribbble', self.gf('django.db.models.fields.CharField')(default='', max_length=80)),
        ))
        db.send_create_signal(u'my_resume', ['SocialPage'])


    def backwards(self, orm):
        # Deleting model 'Resume'
        db.delete_table(u'my_resume_resume')

        # Deleting model 'ResumePositionTag'
        db.delete_table(u'my_resume_resumepositiontag')

        # Deleting model 'ResumeTargetCity'
        db.delete_table(u'my_resume_resumetargetcity')

        # Deleting model 'WorkExperience'
        db.delete_table(u'my_resume_workexperience')

        # Deleting model 'Project'
        db.delete_table(u'my_resume_project')

        # Deleting model 'Education'
        db.delete_table(u'my_resume_education')

        # Deleting model 'Training'
        db.delete_table(u'my_resume_training')

        # Deleting model 'ProfessionalSkill'
        db.delete_table(u'my_resume_professionalskill')

        # Deleting model 'SocialPage'
        db.delete_table(u'my_resume_socialpage')


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
        u'my_resume.education': {
            'Meta': {'object_name': 'Education'},
            'degree': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'educations'", 'to': u"orm['my_resume.Resume']"}),
            'school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'my_resume.professionalskill': {
            'Meta': {'object_name': 'ProfessionalSkill'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'proficiency': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'professional_skills'", 'to': u"orm['my_resume.Resume']"}),
            'skill_desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'})
        },
        u'my_resume.project': {
            'Meta': {'object_name': 'Project'},
            'company_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'project_desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '500'}),
            'project_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'responsible_for': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'projects'", 'to': u"orm['my_resume.Resume']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
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
            'resume_id': ('django.db.models.fields.CharField', [], {'default': "'54b8b4778230db3885bc2cb1'", 'max_length': '50'}),
            'school': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'self_evaluation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '400'}),
            'target_salary': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'work_years': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'my_resume.resumepositiontag': {
            'Meta': {'object_name': 'ResumePositionTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position_tag': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['system.PositionCategoryTag']"}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'position_tags'", 'to': u"orm['my_resume.Resume']"})
        },
        u'my_resume.resumetargetcity': {
            'Meta': {'object_name': 'ResumeTargetCity'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['system.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'expectation_area'", 'to': u"orm['my_resume.Resume']"})
        },
        u'my_resume.socialpage': {
            'Meta': {'object_name': 'SocialPage'},
            'dribbble': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'github': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'resume': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'social_page'", 'unique': 'True', 'to': u"orm['my_resume.Resume']"}),
            'twitter': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'weibo': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'zhihu': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'})
        },
        u'my_resume.training': {
            'Meta': {'object_name': 'Training'},
            'certificate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'course': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '80'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instituation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '60'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trainings'", 'to': u"orm['my_resume.Resume']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'train_desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        u'my_resume.workexperience': {
            'Meta': {'object_name': 'WorkExperience'},
            'company_category': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '30'}),
            'company_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry_category': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'job_desc': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'max_salary': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'min_salary': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'position_category': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'position_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            'resume': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'works'", 'to': u"orm['my_resume.Resume']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'system.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'system.positioncategory': {
            'Meta': {'object_name': 'PositionCategory'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'system.positioncategorytag': {
            'Meta': {'object_name': 'PositionCategoryTag'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['system.PositionCategory']"}),
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }

    complete_apps = ['my_resume']