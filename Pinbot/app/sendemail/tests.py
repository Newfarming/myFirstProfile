# coding: utf-8
from django.test import TestCase
from app.sendemail.runtime.mail_manage import (
    MailTemplateCategoryManage,
    MailTemplateManage,
    MailTagsManage
)
from app.sendemail.models import (
    MailTemplate,
    MailTemplateCategory,
    MailTags
)

from .email_utils import UselessEmailUtils


class TestMailManage(TestCase):

    def setUp(self):

        self.email_category = MailTemplateCategory(
            name='模板分类1'
        )
        self.email_category.save()

        self.email_tpl = MailTemplate(
            category=self.email_category,
            name='邮件标题1',
            content='<p>邮件内容xxx</p>'
        )
        self.email_tpl.save()

        self.tags = MailTags(
            tag_name='标签名称'
        )
        self.tags.save()

    def test_update_email_tpl(self):
        email_tpl = MailTemplateManage.get_all_tpl()[0]
        ret = MailTemplateManage.edit_tpl(
            email_tpl.id,
            email_tpl.category_id,
            '邮件标题1_update',
            '邮件内容_update'
        )
        self.assertIsNotNone(ret, None)

    def test_get_email_tpl(self):
        ret = MailTemplateManage.get_all_tpl()[0]
        self.assertIsNotNone(ret, None)

    def test_get_send_target(self):
        ret = MailTemplateManage.get_send_target(test_users=True,
                                                 b_user=False,
                                                 c_user=False,
                                                 b_unactive_user=False
                                                 )
        self.assertIsNotNone(ret, None)

    def test_get_tag(self):
        ret = MailTagsManage.get_all_tags()[0]
        self.assertIsNotNone(ret, None)

    def test_get_all_category(self):
        ret = MailTemplateCategoryManage.get_all_category()
        self.assertIsNotNone(ret, None)


class TestUselessEmailUtils(TestCase):

    def test_get_useless_email(self):
        useless_email = UselessEmailUtils.get_useless_email()
        self.assertTrue(useless_email)
