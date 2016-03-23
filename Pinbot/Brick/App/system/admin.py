# coding: utf-8

from django.contrib import admin

from .models import (
    City,
    CompanyCategory,
    PositionCategory,
    PositionCategoryTag,
)


class CityAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    search_fields = (
        'name',
    )


class CompanyCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'code_name',
    )
    list_filter = (
        'category',
        'code_name',
    )
    search_field = (
        'category',
    )


class PositionCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code_name',
    )
    list_filter = (
        'name',
        'code_name',
    )
    search_field = (
        'name',
    )


class PositionCategoryTagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code_name',
    )
    list_filter = (
        'name',
    )
    search_field = (
        'name',
    )


admin.site.register(City, CityAdmin)
admin.site.register(CompanyCategory, CompanyCategoryAdmin)
admin.site.register(PositionCategory, PositionCategoryAdmin)
admin.site.register(PositionCategoryTag, PositionCategoryTagAdmin)
