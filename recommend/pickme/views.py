# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
import json
from classes.db import Firebase

# Create your views here.
def space(request):
    fb = Firebase()
    posts = fb.get_initial_posts()
    return JsonResponse(posts)