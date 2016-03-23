# coding: utf-8

import unittest

from .send_mail import MailUtils


class TestMailUtils(unittest.TestCase):

    def test_useless_email(self):
        useless_email = MailUtils.get_useless_email()
        self.assertTrue(useless_email)
