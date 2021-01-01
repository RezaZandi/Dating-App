from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login, logout, authenticate
from dating_app.forms import RegistrationForm,ProfileUpdateForm, MessageForm
from .models import Profile, UserVote, InstantMessage, Conversation
from django.db import models
from django.db.models import Q
from django.db.models import Max
from django.http import JsonResponse


#What I am bringing from sample project 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os
from django.core import serializers
import json
from django.contrib.auth import get_user_model



Profile = get_user_model()


# Create your views here.
def home(request):

	context = {'random_profiles': Profile.objects.exclude(id=request.user.id).order_by('?')[:12]}
	return render(request, 'dating_app/home.html',context)

@login_required
def profiles(request):
	"Shows a list of profiles that have been created"
	profiles = Profile.objects.order_by('date_joined')
	context = {'profiles' : profiles}
	return render(request, 'dating_app/profiles.html',context)

@login_required
def profile(request, profile_id):
	"""show a single profile"""
	profile = get_object_or_404(Profile,id=profile_id)
	context = {'profile' : profile}
	return render(request, 'dating_app/profile.html', context)



# Below is related to users

@login_required
def logout_view(request):
	"""Log out the user """
	logout(request)
	return HttpResponseRedirect(reverse('dating_app:home'))

#original register view, not using anymore
"""
def register(request, profile_id):
	user = User.objects.get(pk=profile_id)
	user.profile.bio = 'fjfjfjjf'
	user.save()
"""

def register(request):
	#Register a new user
	context = {}

	if request.POST:
		form = RegistrationForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get("email")
			description = form.cleaned_data.get("description")
			photo = form.cleaned_data.get("photo")
			raw_password = form.cleaned_data.get('password1')
			profile = authenticate(username=username,email=email,description=description, photo=photo, password=raw_password)
			login(request, profile)
			return redirect ('dating_app:home')
		else:
			context['registration_form'] = form
	else: #get request 
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'dating_app/register.html', context)


@login_required
def update_account(request, profile_id):
	#Edit an existing profile 
	profile = get_object_or_404(Profile,id=profile_id)
	update_form = ProfileUpdateForm(request.POST, request.FILES)
	
	if request.method != 'POST':
		#Initial request; prefil form with current entry
		update_form = ProfileUpdateForm(instance=profile)
	else:
		#POST data submitted;process data. 
		update_form = ProfileUpdateForm(instance=profile, data=request.POST, files=request.FILES)
		if update_form.is_valid():
			update_form.save()
			return HttpResponseRedirect(reverse('dating_app:profile', args=[profile.id]))

	context = {'profile' : profile, 'update_form' : update_form}
	return render(request, 'dating_app/update.html', context)



#matching
@login_required
def mingle(request):
	


	try:
	 	profile = (Profile.objects.exclude(id=request.user.id).exclude(uservote__voter=request.user).order_by('?')[0])
	except IndexError:
		profile = None
		print(Profile.username)
	try:
		
		description = request.user.description
	except Profile.DoesNotExist:
		create = Profile.objects.get_or_create(request.user)
		return redirect('profile')

	match = request.user.matches.all()
	context = dict(profile = profile, match = match)	
	return render(request, 'dating_app/mingle.html', context)



@login_required
def nice(request, profile_id):

	return create_vote(request, profile_id, True)

@login_required
def nope(request, profile_id):
	return create_vote(request, profile_id, False)




@login_required
def create_vote(request, profile_id, vote):
    profile = get_object_or_404(Profile, pk=profile_id)

    
    UserVote.objects.create(
        user=profile,
        voter=request.user,
        vote=vote
    )
    other = UserVote.objects.filter(
        voter=profile,
        user=request.user,
        vote=True
    )
    if vote and other.exists():
        profile.matches.add(request.user)
        request.user.matches.add(profile)
        return render(request, 'dating_app/match.html', dict(
				match=profile,
			))
    return redirect('dating_app:mingle')


@login_required
def view_matches(request,profile_id):
	match = request.user.matches.all()
	profile = get_object_or_404(Profile,id=profile_id)
	print(profile)
	
	context = {'match' : match, 'profile' : profile}

	return render(request, 'dating_app/matches.html', context)


@login_required
def messages(request,profile_id):

	other_user = get_object_or_404(Profile,id=profile_id)

	if profile == request.user:
		raise Http404
	
	exclusive_conversations = Conversation.objects.filter(members= request.user ).filter(members= other_user)
	messages = InstantMessage.objects.filter(conversation__in=exclusive_conversations)




	for message in messages:
		if message.sender != request.user:
			
			message.viewed=True

			message.save()

	context = {'messages' : messages, 'other_user' : other_user}

	return render(request, 'dating_app/messages.html', context)


@login_required
def conversations(request,profile_id):

	


	conversations = Conversation.objects.filter(
		members=profile_id
	).annotate(
		last_message=Max('instantmessage__date')
	).prefetch_related('members').order_by(
		'-last_message'
	)


   
	return render(request, 'dating_app/conversations.html', {'conversations':conversations,})



#newform for message
@login_required
def message (request, profile_id):

	if request.method == 'POST':

		form = MessageForm(request.POST)
		if form.is_valid():
			form.save()
			
		
			return redirect('dating_app:messages', profile_id)
	else:
		#get or creates a convo object
		conversation, created = Conversation.objects.filter(members = request.user).filter(members= profile_id).get_or_create()
		#adds the two users in, since it's a many to many field field 
		conversation.members.add(request.user, profile_id)
	
		other_user = conversation.members.filter(id=profile_id).get()
		
		form = MessageForm({'sender': request.user, 'receiver':profile_id, 'conversation': conversation})
		
		context = {'form' : form, 'other_user': other_user }
		return render(request, 'dating_app/message.html', context)


def check_if_username_exists_view(request):
	username = request.GET.get('username', None)
	data = {
		'is_taken': Profile.objects.filter(username__iexact=username).exists()
		}
	return JsonResponse(data)

