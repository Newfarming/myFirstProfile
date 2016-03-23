# coding: utf-8

from .models import (
    Company,
)

class JobUtils(object):

    @classmethod
    def has_fill_company(cls, user):
        company_query = Company.objects.prefetch_related(
            'category'
        ).filter(
            user=user
        )

        if not company_query:
            return False

        company = company_query[0]
        return company if (
            company.company_name
            and company.key_points
            and company.desc
            and company.company_stage
            and company.url
            and company.category.all()
        ) else False