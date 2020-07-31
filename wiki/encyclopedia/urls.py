from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('random', views.random, name='random'),
    path('<str:title>', views.entry, name='entry'),
]
