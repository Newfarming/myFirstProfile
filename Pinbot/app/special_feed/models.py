# coding: utf-8

from mongoengine import *


class SpecialFeed(DynamicDocument):
    username = StringField(max_length=50, required=True)
