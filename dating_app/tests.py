from django.test import TestCase

from .models import Profile,InstantMessage, Conversation




class InstantMessageTestCase(TestCase):
	



	def test_messages_find_messages_exclusive_to_profile(self):


		sending_user = Profile.objects.create(username="sender", photo="l", description="s", email="jfklhfh@yahoo.com")
		receiving_user = Profile.objects.create(username="recepient", photo="l", description="s", email="jjjfklhfh@yahoo.com")
		unrelated_user = Profile.objects.create(username="unrelated_user", photo="l", description="s", email="jjjjjfklhfh@yahoo.com")


		relevant_conversation= Conversation.objects.create()
		relevant_conversation.members.add(sending_user,receiving_user)

		unrelevant_conversation = Conversation.objects.create()
		unrelevant_conversation.members.add(sending_user,unrelated_user)


		relevant_message = InstantMessage.objects.create(sender=sending_user, receiver= relevant_conversation, message= 'sending message',)
		relevant_message_opposite = InstantMessage.objects.create(sender=receiving_user, receiver=relevant_conversation, message= 'receiver is sending the message' )

		unrelevant_message = InstantMessage.objects.create(sender=sending_user, receiver= unrelevant_conversation, message= 'sending to unrelated user',)



		exclusive_messages = InstantMessage.find_messages_exclusive_to_profile(sender=sending_user, receiver= receiving_user)

		self.assertEqual(relevant_message, exclusive_messages[0])

		self.assertEqual(relevant_message_opposite, exclusive_messages[1])


		

		


