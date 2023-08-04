from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('home/', views.home, name='home'),
    path('login_user/', views.login_view, name='login_view'),
    path('logout_user/', views.logout_view, name='logout_user'),
    path('client_list/', views.client_list, name='client_list'),
     path('client_detail/<int:id_client>', views.client_detail, name='client_detail'),
    path('register/', views.create_client, name='register'),
    path('services_view/', views.services_view, name='services_view'),
    path('create_quote/', views.create_quote, name='create_quote'),
    path('quote/', views.create_quote, name='quote'),
    path('quote2/', views.quote2_view, name='quote2'),
    path('quote3/', views.quote3_view, name='quote3'),
    path('quote4/', views.quote4_view, name='quote4'),
    path('quote5/', views.quote5_view, name='quote5'),    
    path('load_csv/', views.load_csv, name='load_csv'),
    path('load_cities/', views.load_cities, name='load_cities'),
    path('load_airlines/', views.load_airlines, name='load_airlines'),
    path('load_hotels/', views.load_hotels, name='load_hotels'),
    
]