from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["name", "username", "email", "password1", "password2"]


class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = (
            "host",
            "participants",
        )
        fields = "__all__"


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username", "email", "name", "avtar", "bio")
