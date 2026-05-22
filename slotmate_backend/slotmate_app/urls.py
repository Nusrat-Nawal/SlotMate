from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page),
    path('login/', views.login_page),
    path('register/', views.register_page),
    path('index/',views.index),
    path('create-request/', views.create_request_page),
    path('forget-password/', views.forget_password_page),
    path('my-requests/', views.my_requests_page),
    path('matches/', views.matches_page),
    path('notifications/', views.notifications_page),
    path('profile/', views.profile_page)
]