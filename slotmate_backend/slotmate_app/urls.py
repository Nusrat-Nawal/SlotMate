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
    path('notifications/', views.notifications_page),
    path("delete-multiple/", views.delete_multiple, name="delete_multiple"),
    path("delete-request/<int:request_id>/", views.delete_request, name="delete_request"),
    path("matches/", views.matches_list_page, name="matches"),
    path("match/<int:match_id>/", views.match_detail_page, name="match_detail"),
    path("profile/", views.profile_page),
    path("profile/update/",views.update_profile),
    path("profile/change-password/", views.change_password),
    path('logout/', views.logout_view),
    path('send-verification/', views.send_verification_email, name='send_verification'),
    path("reveal/send/<int:match_id>/", views.send_reveal_request),
    path("reveal/respond/<int:match_id>/", views.respond_reveal_request, name="respond_reveal"),
    path("notification/delete/<int:notification_id>/", views.delete_notification),
    path("reveal/accept/<int:reveal_id>/", views.accept_reveal, name="accept_reveal"),
    path("reveal/reject/<int:reveal_id>/", views.reject_reveal, name="reject_reveal"),
]