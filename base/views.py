from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import RoomForm, UserForm
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def loginPage(request):

    page = "login"

    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "user does not exists")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "User or Password does not exists")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


def registerUser(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # messages.success("Register Sucessfully. Now you can login")
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, form.errors)

    context = {"form": form}
    return render(request, "base/login_register.html", context)


def home(request):

    q = request.GET.get("q") if request.GET.get("q") != None else ""

    room = Room.objects.filter(
        Q(topic__name__icontains=q)
        | Q(name__icontains=q)
        | Q(host__username__icontains=q)
        | Q(description__icontains=q)
    )

    room_count = room.count()  # faster then len method
    # roomcount=len(room)

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    pupularTopic = Topic.objects.annotate(room_count=Count("room")).order_by(
        "-room_count"
    )[:10]
    context = {
        "rooms": room,
        "topics": pupularTopic,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by("-created")
    participants = room.participants.all()
    if request.method == "POST":
        comment = Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)
        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "base/room.html", context)


def userProfile(request, pk):

    profile = User.objects.get(id=pk)
    rooms = profile.room_set.all()
    room_count = rooms.count()
    room_messages = profile.message_set.all()
    topics = Topic.objects.all()
    context = {
        "user": profile,
        "rooms": rooms,
        "room_count": room_count,
        "topics": topics,
        "room_messages": room_messages,
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("home")

    context = {"form": form, "topics": topics}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not authorized")

    if request.method == "POST":
        topic_name = request.POST.get("topic")
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get("name")
        room.host = request.user
        room.topic = topic
        room.description = request.POST.get("description")

        room.save()
        return redirect("home")

    context = {"form": form, "topics": topics, "room": room}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect("home")
    context = {"obj": room}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.method == "POST":
        message.delete()
        return redirect("home")
    context = {"obj": message}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        print("sdffsssssss")
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            print("Everythin is saved")
            return redirect("user-profile", pk=user.id)
        else:
            print(form.errors)

    context = {"form": form}
    return render(request, "base/update-user.html", context)


def topicsPage(request):
    q = request.GET.get("q") if request.GET.get("q") is not None else ""

    if q:
        topics = Topic.objects.filter(name__icontains=q)
    else:
        topics = Topic.objects.order_by("?")[:5]

    context = {"topics": topics}

    return render(request, "base/topics.html", context)


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, "base/activity.html", {"room_messages": room_messages})
