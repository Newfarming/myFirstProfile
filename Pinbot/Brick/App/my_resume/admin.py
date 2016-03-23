# coding: utf-8

from django.contrib import admin

from .models import (
    Resume,
    ResumeTargetCity,
    ResumePositionTag,
    WorkExperience,
    Project,
    Education,
    Training,
    ProfessionalSkill,
    SocialPage,
)


class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'gender',
        'job_category',
        'work_years',
    )
    search_field = (
        'user',
        'name',
    )


class ResumeTargetCityAdmin(admin.ModelAdmin):
    list_display = (
        'resume',
        'city',
    )
    search_field = (
        'resume',
    )


class ResumePositionTagAdmin(admin.ModelAdmin):
    list_display = (
        'resume',
        'position_tag',
    )
    search_field = (
        'resume',
    )


class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = (
        'resume',
        'position_title',
        'company_name',
    )


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'resume',
        'responsible_for',
    )


class EducationAdmin(admin.ModelAdmin):
    list_display = (
        'resume',
        'school',
        'degree',
        'major',
    )
    search_fields = (
        'resume',
    )


class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        'resume',
        'course',
        'instituation',
    )
    search_fields = (
        'resume',
        'instituation',
    )


class ProfessionalSkillAdmin(admin.ModelAdmin):
    list_display = (
        'resume',
        'skill_desc',
        'proficiency',
    )


class SocialPageAdmin(admin.ModelAdmin):
    list_display = (
        'resume',
        'github',
        'zhihu',
        'dribbble',
    )


admin.site.register(Resume, ResumeAdmin)
admin.site.register(ResumeTargetCity, ResumeTargetCityAdmin)
admin.site.register(ResumePositionTag, ResumePositionTagAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(ProfessionalSkill, ProfessionalSkillAdmin)
admin.site.register(SocialPage, SocialPageAdmin)
