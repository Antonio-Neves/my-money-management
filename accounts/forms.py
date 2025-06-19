from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

from accounts.models import CustomUser


class CustomUserCreateForm(UserCreationForm):

	class Meta():
		model = CustomUser
		fields = ('first_name', 'last_name', 'email')
		labels = {'email': 'Username/Email'}

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.email = self.cleaned_data["email"]

		if commit:
			user.save()

		return user


class CustomUserChangeForm(UserChangeForm):

	class Meta():
		model = CustomUser
		fields = ('first_name', 'last_name', 'email')

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data["email"]

		if commit:
			user.save()

		return user
