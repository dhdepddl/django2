# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .classes.Post import PostDB
from .classes.User import UserDB

# Register your models here.


admin.site.register(PostDB)
admin.site.register(UserDB)
