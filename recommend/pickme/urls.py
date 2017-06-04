from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^space/', views.space, name='space'),
    url(r'^cards/', views.cards, name='cards')
]