from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name='login'),       
    path('signup/', views.signup_view, name='signup'),  
]
