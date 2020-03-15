

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from django.contrib.auth import logout
from django.contrib.auth import login, logout, authenticate
from dating_app.forms import RegistrationForm,ProfileUpdateForm
from .models import Profile

# Create your views here.
def home(request):

	return render(request, 'dating_app/home.html')


def profiles(request):
	"Shows a list of profiles that have been created"
	profiles = Profile.objects.order_by('date_joined')
	context = {'profiles' : profiles}
	return render(request, 'dating_app/profiles.html',context)

	
def profile(request, profile_id):
	"""show a single profile"""
	profile = get_object_or_404(Profile,id=profile_id)
	context = {'profile' : profile}
	return render(request, 'dating_app/profile.html', context)



# Below is what i am bringing from users


def logout_view(request):
	"""Log out the user """
	logout(request)
	return HttpResponseRedirect(reverse('dating_app:home'))


def register(request, profile_id):
	user =User.objects.get(pk=profile_id)
	user.profile.bio = 'fjfjfjjf'
	user.save()


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



def update_account(request, profile_id):
	#Edit an existing profile 
	profile = get_object_or_404(Profile,id=profile_id)
	update_form = ProfileUpdateForm(request.POST, request.FILES)
	#check_profile_owner(profile.owner,request.user)

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


"""Checks to see if the current user is also the profile owner"""
#def check_profile_owner(user):
 
    # if owner != user:
       # raise Http404 



"""
	if request.method == 'POST':
		#Display blank regisration form. 
		user_form = UserForm(request.POST, instance=request.user)
		profile_form = ProfileForm(request.POST, instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, _('Yourprofile was succesfuly created'))
			return HttpResponseRedirect(reverse('dating_app:home'))
		else:
			messages.error(request,_('please correct'))
	else:
		#Process completed form.
		user_form = UserForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)

	context = {'user_form': user_form, 'registration_form' : registration_form}


	return render(request, 'dating_app/register.html', context)

"""
