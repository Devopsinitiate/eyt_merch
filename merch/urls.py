from django.urls import path
from . import views

app_name = 'merch'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/sizes/', views.get_available_sizes, name='available_sizes'),
    path('api/order/', views.create_order, name='create_order'),
]