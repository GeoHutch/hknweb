from django import forms
from hknweb.users.models import CustomUser as User
from hknweb.users.models import CustomUserProfile as Profile

class SettingsForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('picture', 'private', 'phone_number', 'date_of_birth', 'resume', 'graduation_date')
