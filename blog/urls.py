from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('explore/', views.explore_view, name='explore'),
    path('create/', views.create_post_view, name='create_post'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/delete/', views.delete_post, name='delete_post'),
] 
