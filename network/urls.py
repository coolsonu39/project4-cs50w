
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("newpost", views.newpost, name="newpost"),
    path("user/<int:userid>", views.userpage, name="userpage"),
    path("followfeed", views.followfeed, name="followfeed"),

    path("togglelike/<int:postid>", views.togglelike, name="togglelike"),
    path("editpost", views.editpost, name="editpost"),
    path("togglefollow/<int:userdisid>", views.togglefollow, name="togglefollow")
]
