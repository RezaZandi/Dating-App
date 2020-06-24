"""Defines url patterns for dating_app"""

from django.urls import path
from django.contrib.auth.views import LoginView
from . import views 


app_name = 'dating_app'
urlpatterns = [
#Home page
	path('', views.home, name='home'),
#List of profiles
	path('profiles/', views.profiles, name='profiles'),
#Individual profiles
	path('profile/<int:profile_id>/', views.profile, name='profile'),


#Reg/Login page
	path('login/', LoginView.as_view(template_name = 'dating_app/login.html'), name='login'),
	#Logout page
	path('logout/', views.logout_view, name='logout'),
	#Registration page 
	path('register/', views.register, name='register'),
	path('ajax/check_if_username_exists_view/', views.check_if_username_exists_view, name='check_if_username_exists_view'),

#edit profile
	path('update_account/<int:profile_id>/', views.update_account, name='update_account'),

#Matching 
	path('mingle/', views.mingle, name='mingle'),
	path('view_matches/<int:profile_id>/', views.view_matches, name='view_matches'),

#like or dislike
	path('nice/<int:profile_id>/', views.nice, name='nice'),
	path('nope/<int:profile_id>/', views.nope, name='nope'),


#messaging
	#message form
	path('message/<int:profile_id>/', views.message, name='message'),
	#displays messages in a single conversation
	path('messages/<int:profile_id>/', views.messages, name='messages'),
	#displays active conversations
	path('conversations/<int:profile_id>/', views.conversations, name='conversations'),
]