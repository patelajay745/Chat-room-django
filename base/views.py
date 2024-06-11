from django.shortcuts import render
from .models import Room


# Create your views here.

def home(request):
    
    context={'rooms':Room.objects.all}
    return render(request,'base/home.html',context)

def room(request,pk):
    

    context={'room':Room.objects.get(id=pk)}
    return render(request,'base/room.html',context)