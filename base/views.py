from django.shortcuts import render
from .models import Room


# Create your views here.

def home(request):
    
    context={'rooms':Room.objects.all}
    return render(request,'base/home.html',context)

def room(request,pk):
    room=None
    for i in Room.objects.all:
        if i['id']==int(pk):
            room=i

    context={'room':room}
    return render(request,'base/room.html',context)