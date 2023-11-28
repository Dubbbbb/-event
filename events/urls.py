from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("+event", views.create_event, name="create_event"),
    path("+event/<int:event_id>", views.event_details, name="event_details"),
    path('+task', views.create_task_to_todo_list, name="create_task"),
    path('+item', views.create_item_to_price_list, name="create_item"),
    path('+user/<int:event_id>/', views.invite_users_to_event, name='invite_users'),
    path('-user/<int:event_id>/', views.uninvite_users_to_event, name='uninvite_users'),
    path('notifications', views.notifications_detail, name='notifications'),
    path('check_notification', views.check_notification, name='check_notification'),
    path('check_task', views.check_task, name='check_task'),
    path('change_event_public', views.change_event_public, name='change_event_public'),




    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
