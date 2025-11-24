# -*- encoding: utf-8 -*-

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    # Cell visualization page
    path('cells/', views.cells, name='cells'),

    # People pages
    path('people/', views.people, name='people'),
    path('profile/<str:username>/', views.profile, name='profile'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
