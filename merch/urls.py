from django.urls import path
from . import views

app_name = 'merch'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('api/sizes/', views.get_available_sizes, name='available_sizes'),
    path('api/order/', views.create_order, name='create_order'),
]