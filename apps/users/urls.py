from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.show_register_page, name='register-page'),
    path('login/', views.show_login_page, name='login-page'),
    path('logout/', views.user_logout, name='user-logout'),
    path('me/', views.show_profile_page, name='user-profile'),
    path('me/edit/', views.edit_profile_page, name='edit-profile'),
    path('me/subscribers/', views.show_subscribers_page, name='subscribers-page'),
    path('<int:user_id>/follow/', views.follow_user, name='follow-user'),
    path('<int:user_id>/unfollow/', views.unfollow_user, name='unfollow-user'),
]

