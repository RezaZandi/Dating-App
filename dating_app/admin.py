from django.contrib import admin
from dating_app.models import Profile,UserVote,InstantMessage,Conversation

admin.site.register([Profile,UserVote,InstantMessage,Conversation])