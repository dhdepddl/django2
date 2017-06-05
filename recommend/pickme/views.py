# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from classes.db import Firebase
from multiprocessing import Process, Queue
import time


def space(request):
    output = Queue()
    p = Process(target=space_work, args=(request, output))
    p.start()
    posts = output.get()
    return JsonResponse(posts)


def space_work(request, output):
    user_id = request.path.replace('/', '').replace('space', '')
    fb = Firebase(user_id)
    fb.get_all_data()
    posts = fb.get_cards(user_id, 5)
    output.put(posts)


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
    fb.get_all_data()
    post = fb.get_card_with_id(user_id, post_id)
    return JsonResponse(post)


def get_topic(request):
    fb = Firebase(u'')
    fb.get_topic()
    return JsonResponse({})
