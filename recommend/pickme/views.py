# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render
from django.http import JsonResponse
import json
from classes.db import Firebase


def space(request):
    user_id = request.path.replace('/', '').replace('space', '')
    fb = Firebase(user_id)
    posts = fb.get_cards(user_id, 5)
    return JsonResponse(posts)