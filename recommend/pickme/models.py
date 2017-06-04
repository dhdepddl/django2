# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField


class Post(models.Model):
    post_id = models.CharField(max_length=30, primary_key=True)
    user_id = models.CharField(max_length=30)
    topic = models.SmallIntegerField()
    topic_2 = models.SmallIntegerField()

    def __str__(self):
        return self.post_id