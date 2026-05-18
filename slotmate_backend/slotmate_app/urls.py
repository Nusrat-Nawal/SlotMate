from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_page),
    path('register/', views.register_page),
    path('create-request/', views.create_request_page),
     path('forget-password/', views.forget_password_page),

]