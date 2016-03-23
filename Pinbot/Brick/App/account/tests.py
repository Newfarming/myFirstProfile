# coding: utf-8

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


c = Client()


class TestAccounnt(TestCase):

    def test_check_user_status(self):
        url = reverse('account-check-user-status')
        res = c.post(url)
        self.assertEqual(res.status_code, 200)

    def test_register(self):
        url = reverse('account-register')
        res = c.post(url)
        self.assertEqual(res.status_code, 200)

    def test_send_active_email(self):
        url = reverse('account-send-active-email', args=('runforever@163.com',))
        res = c.get(url)
        self.assertEqual(res.status_code, 200)

    def test_valid_email(self):
        url = reverse('account-valid-active-email', args=('runforever@163.com',))
        res = c.get(url)
        self.assertEqual(res.status_code, 200)

    def test_change_password(self):
        url = reverse('account-change-password')
        User.objects.create_user(
            'admin',
            'admin',
            'admin',
        )
        self.client.login(username='admin', password='admin')
        res = self.client.post(url)
        self.assertEqual(res.status_code, 200)
        self.client.logout()

    def test_reset_email(self):
        url = reverse('account-reset-password', args=('fadfasfd',))
        res = c.get(url)
        self.assertEqual(res.status_code, 200)
