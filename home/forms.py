from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import Member

class MemberCreationForm(UserCreationForm):
    phone = forms.IntegerField(required=False)
    class Meta:
        model = Member
        fields = ("email", "password1", "password2", "phone", "status")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # remove the username since it's not a part of the Member model
        if 'username' in self.fields:
            del self.fields['username']

class MemberChangeForm(UserChangeForm):
    class Meta:
        model = Member
        fields = ("email",)