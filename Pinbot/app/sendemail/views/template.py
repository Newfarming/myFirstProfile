# coding: utf-8

from django.views.generic import View, ListView
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from ..models import (
    MailTemplate,
    MailTemplateCategory
)
from ..runtime.mail_manage import (
    MailTemplateManage,
    MailTemplateCategoryManage
)

from pin_utils.django_utils import (
    JsonResponse,
    get_object_or_none,
    get_int,
    get_float,
)

from pin_utils.mixin_utils import (
    CSRFExemptMixin,
    StaffRequiredMixin
)


class GetEmailTemplate(StaffRequiredMixin, View):
    """获取邮件模板"""
    def get(self, request, tpl_id):
        tpl_manage = MailTemplateManage()
        template = tpl_manage.get_tpl(id=tpl_id)
        return JsonResponse({
                            'template_content': template.content,
                            'template_title': template.name,
                            'category_id': template.category.id})


class AddEmailTemplate(StaffRequiredMixin, View, MailTemplateManage):
    """添加邮件模板"""
    template_name = 'add_template.html'

    def get(self, request):
        form = MailTemplateManage(request=request)
        return render(
            request,
            self.template_name,
            {
                'form': form
            }
        )

    def post(self, request):

        form = MailTemplateManage(request.POST, request=request)
        if form.is_valid():
            form.add_tpl()
            result = {'status': 'ok', 'msg': '添加模板成功!'}
        else:
            result = {
                'status': 'form_error',
                'msg': form.get_first_errors()
            }

        return JsonResponse(result)


class EditEmailTemplate(StaffRequiredMixin, CSRFExemptMixin, View):
    """编辑邮件模板"""
    template_name = 'edit_template.html'

    def get(self, request, tpl_id):
        mailTplManage = MailTemplateManage()
        form = MailTemplateManage(request=request)
        template_obj = get_object_or_none(
            MailTemplate,
            id=tpl_id,
        )
        all_template = mailTplManage.get_all_tpl()
        return render(
            request,
            self.template_name,
            {
                'template_obj': template_obj,
                'form': form,
                'all_template': all_template
            }
        )

    def post(self, request, tpl_id):

        category_id = request.POST['category']
        name = request.POST['name']
        content = request.POST['content']

        ret = MailTemplateManage.edit_tpl(tpl_id=tpl_id, category_id=category_id, template_name=name, template_content=content)
        if ret:
            result = {
                'status': 'ok',
                'msg': '更新邮件模板成功!'
            }
        else:
            result = {
                'status': 'form_error',
                'msg': '更新邮件模板失败'
            }

        return JsonResponse(result)


class AddEmailTemplateCategory(StaffRequiredMixin, View):
    """添加邮件模板分类"""
    template_name = 'add_template_category.html'

    def get(self, request):
        mcm = MailTemplateCategoryManage()
        all_category = mcm.get_all_category()
        return render(
            request,
            self.template_name,
            {
                'all_category': all_category
            }
        )

    def post(self, request):

        form = MailTemplateCategoryManage(request.POST, request=request)

        if form.is_valid():
            form.add_tpl_category()
        return redirect('/email/add_tpl_category')


class EditEmailTemplateCategory(StaffRequiredMixin, View):
    """更新邮件模板分类"""
    template_name = 'edit_template_category.html'

    def get(self, request, cid):
        mcm = MailTemplateCategoryManage()
        all_category = mcm.get_all_category()

        category_obj = get_object_or_none(
            MailTemplateCategory,
            id=cid,
        )

        return render(
            request,
            self.template_name,
            {
                'category_obj': category_obj,
                'all_category': all_category
            }
        )

    def post(self, request, cid):

        category_obj = get_object_or_none(
            MailTemplateCategory,
            id=cid,
        )

        form = MailTemplateCategoryManage(request.POST, request=request) if not category_obj else MailTemplateCategoryManage(request.POST, instance=category_obj, request=request)

        if form.is_valid():
            category = form.save(commit=False)
            category.name = form.cleaned_data['name']
            category.save()
            result = {'status': 'ok', 'msg': '更新模板分类成功!'}
        else:
            result = {
                'status': 'form_error',
                'msg': form.get_first_errors()
            }

        return JsonResponse(result)