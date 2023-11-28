import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


from .models import User, Event, TodoListTask, PriceListItem, Notification
from .forms import InviteUserForm
from .tasks import create_invite_notification, create_uninvite_notification


def index(request):
    events = Event.objects.filter(is_public=True).order_by('-created_at')
    return render(request, "index.html", {'events': events})


@login_required
def profile(request):
    events = Event.objects.filter(creator=request.user)
    return render(request, 'profile.html', {'events': events})


@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        is_public = True if 'is_public' in request.POST else False
        new_event = Event.objects.create(title=title, is_public=is_public, creator=request.user)
        new_event.save()
        return redirect('profile')
    elif request.method == 'GET':
        return render(request, '+event.html', {})


def event_details(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user == event.creator or event.is_public:
        users = User.objects.all()
        return render(request, 'event_details.html', {'event': event, 'users': users})
    else:
        return redirect('profile')


@login_required
def create_task_to_todo_list(request):
    task_text = request.POST['text']
    todo_list_id = request.POST['todo_list_id']
    new_task = TodoListTask.objects.create(text=task_text, todo_list_id=todo_list_id)
    new_task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def create_item_to_price_list(request):
    name = request.POST['name']
    price = request.POST['price']
    price_list_id = request.POST['price_list_id']
    new_item = PriceListItem.objects.create(name=name, price=price, price_list_id=price_list_id)
    new_item.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def invite_users_to_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = InviteUserForm(request.POST)
    if form.is_valid():
        invited_users = form.cleaned_data['users']
        event.users.add(*invited_users)
        create_invite_notification(invited_users, event.title)
        return redirect('event_details', event_id=event.pk)



@login_required
@csrf_exempt
def uninvite_users_to_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    data = json.loads(request.body)
    user_id = int(data.get('user_id'))
    event.users.remove(user_id)
    create_uninvite_notification(user_id, event.title)
    return JsonResponse({"message": 'OK'}, status=200)



@login_required
def notifications_detail(request):
    notifications = request.user.notification.all().order_by('-created_at')
    return render(request, 'notification.html', {'notifications': notifications})


@login_required
@csrf_exempt
def check_notification(request):
    data = json.loads(request.body)
    notif_id = int(data.get('notification_id'))
    notification = Notification.objects.get(pk=notif_id)
    notification.checked = True
    notification.save()
    return JsonResponse({
                "notification_count": request.user.notification.filter(checked=0).count()
            }, status=200)


@login_required
@csrf_exempt
def check_task(request):
    data = json.loads(request.body)
    task_id = int(data.get('task_id'))
    status = data.get('status')
    task = TodoListTask.objects.get(pk=task_id)
    task.status = status
    task.save()
    return HttpResponse(status=200)


@login_required
@csrf_exempt
def change_event_public(request):
    data = json.loads(request.body)
    event_id = int(data.get('event_id'))
    is_public = data.get('is_public')
    event = Event.objects.get(pk=event_id)
    event.is_public = is_public
    event.save()
    return HttpResponse(status=200)






# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")