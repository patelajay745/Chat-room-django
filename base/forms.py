from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


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
        fields = ("username", "email", "first_name", "last_name")
