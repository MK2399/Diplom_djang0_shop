from django.urls import path
from .views import *

urlpatterns = [
    path('', product_list, name='product_list'),
    path('catalog/<slug:category_slug>/', product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>', product_detail, name='product_detail'),
]