# coding: utf-8

from pymongo import MongoClient
from Brick.settings import MONGO_URI

Mongo = MongoClient(MONGO_URI)
