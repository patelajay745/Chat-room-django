from django.shortcuts import render,redirect
from .models import Room,Topic
from .forms import RoomForm
from django.db.models import Count


# Create your views here.

def home(request):

    q=request.GET.get('q')
    room=Room.objects.all()
    if q is not None:
        room=Room.objects.filter(topic__name__icontains=q)

    pupularTopic=Topic.objects.annotate(room_count=Count('room')).order_by('-room_count')[:10]
    context={'rooms':room,'topics':pupularTopic}    
    return render(request,'base/home.html',context)

def room(request,pk):
    context={'room':Room.objects.get(id=pk)}
    return render(request,'base/room.html',context)

def createRoom(request):
    form=RoomForm()
    if request.method=='POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)

def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.method=='POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context={'form':form}
    return render(request,'base/room_form.html',context)

def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('home')
    context={'room':room}
    return render(request,'base/delete_room.html',context)
