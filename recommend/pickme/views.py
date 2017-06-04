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


def cards(request):
    info = request.path.replace('/cards/', '').replace('cards/', '').split('/')
    if len(info) == 0:
        return JsonResponse({})
    post_id = info[0]
    if len(info) == 1:
        user_id = u''
    else:
        user_id = info[1]
    fb = Firebase(user_id)
    post = fb.get_card_with_id(user_id, post_id)
    return JsonResponse(post)