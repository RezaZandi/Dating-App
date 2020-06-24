from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, User
from dating_project import settings
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone



class ProfileManager(BaseUserManager):



	def create_user(self, username, email,description,photo, password=None):
		if not email:
			raise ValueError("You must creat an email")
		if not username:
			raise ValueError("You must create a username!")
		if not description:
			raise ValueError("You must write a description")
		if not photo:
			raise ValueError("You must upload a photo")

		user = self.model(
				email=self.normalize_email(email),
				username = username, 
				description= description,
				photo= photo,
			
			)

		user.set_password(password)
		user.save(using=self._db)
		return user 


	def create_superuser(self, username, email,description,photo, password):
		user = self.create_user(
				email=self.normalize_email(email),
				password=password,
				username=username,
				description=description,
				photo=photo,
				
			)

		user.is_admin=True
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user
	



class Profile(AbstractBaseUser):

	class Meta:
		swappable = 'AUTH_USER_MODEL'


	email 						= models.EmailField(verbose_name="email")
	username					= models.CharField(max_length=30, unique=True)
	date_joined					= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login					= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin					= models.BooleanField(default=False)
	is_active					= models.BooleanField(default=True)
	is_staff					= models.BooleanField(default=False)
	is_superuser				= models.BooleanField(default=False)
	#what I added
	description 				= models.TextField()
	photo 						= models.ImageField(upload_to='profile_photo',blank=False, height_field=None, width_field=None, max_length=100)
	matches 					= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='+', blank=True)
			


	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['description','photo','email']


	objects = ProfileManager()


	def __str__(self):
		return self.username


	def has_perm(self, perm, obj=None):
		return self.is_admin


	def has_module_perms(self,app_label):
		return True

		

class Conversation(models.Model):
    members = models.ManyToManyField(settings.AUTH_USER_MODEL)


class UserVote(models.Model):
	
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	voter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='given_vote', on_delete=models.CASCADE)
	vote = models.BooleanField(default=False)

	class Meta:
		unique_together = (('user', 'voter'))




    

class InstantMessage(models.Model):

	
	sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name= 'sender',on_delete=models.CASCADE )
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name= 'receiver',on_delete=models.CASCADE )
	conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
	message = models.TextField()
	date = models.DateTimeField(verbose_name="Data creation",default=timezone.now, null=False)
	viewed = models.BooleanField(default=False, db_index=True)


	def __unicode__(self):
		return self.message

	#tests to see if messages are exclusive between sender, receiver (won't work with new model)
	@classmethod
	def find_messages_exclusive_to_profile(cls,sender,receiver):
		#members = receiver AND sender, not receiver or sender 
		exclusive_conversations = Conversation.objects.filter(members= receiver ).filter(members= sender)


		exclusive_messages = InstantMessage.objects.filter(conversation__in=exclusive_conversations)

		return exclusive_messages







