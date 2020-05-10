
from django import forms
from django.contrib.auth.forms import UserCreationForm

from dating_app.models import Profile,InstantMessage




class RegistrationForm(UserCreationForm):
	

	class Meta:
		model = Profile 
		fields = ("username","email","description","photo","password1","password2")





class ProfileUpdateForm(forms.ModelForm):

	class Meta:
		model = Profile 
		fields = ('username','description','photo')


	def clean_username(self):
		
		if self.is_valid():
			username = self.cleaned_data['username']
			#makes sure no two users have same username
			try:
				profile = Profile.objects.exclude(pk=self.instance.pk).get(username=username)
			except Profile.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use. Please pick another username!' % profile.username)

	def clean_description(self):
		if self.is_valid():
			#doesn't matter if descriptions are the same
			description = self.cleaned_data['description']
			return description


	def clean_photo(self):
		if self.is_valid():
			photo = self.cleaned_data['photo']
			return photo
			

class MessageForm(forms.ModelForm):

	class Meta:
		model = InstantMessage
		fields = ('sender','conversation','message','receiver')
		widgets = {'sender': forms.HiddenInput(), 'conversation': forms.HiddenInput(), 'receiver': forms.HiddenInput()}
		


