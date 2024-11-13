from django.urls import path
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Course related URLs
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('courses/<int:course_id>/content/', views.course_content, name='course_content'),
    path('modules/<int:module_id>/progress/', views.update_progress, name='update_progress'),
    path('course/<int:course_id>/review/', views.course_review, name='course_review'),
    path('module/<int:module_id>/download/', views.download_file, name='download_file'),
    path('module/<int:module_id>/quiz/', views.quiz_view, name='quiz_view'),
    path('module/<int:module_id>/results/', views.quiz_results, name='quiz_results'),
    # Other URL patterns...
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
]