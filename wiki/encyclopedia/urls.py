from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('random', views.random, name='random'),
    path('new_entry', views.new_entry, name='new_entry'),
    path('edit_entry', views.edit_entry, name='edit_entry'),
    path('<str:title>', views.entry, name='entry'),
]
