from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name = 'homePage'),
    path('all-categories', all_categories, name = 'all-categoriesPage'),
    path('category/<str:search_word>', search_category, name="searchCategory"),
]