from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    allpost = Post.objects.order_by("-timestamp").all()
    paginator = Paginator(allpost, 10)
    page = request.GET.get('page')

    return render(request, "network/index.html", {
        "allposts": paginator.get_page(page)
    })

@login_required(login_url='login')
def newpost(request): # only accepts post request
    post = Post(content=request.POST["content"], author=User.objects.get(pk=request.user.pk))
    post.save()
    return HttpResponseRedirect(reverse('index'))

@login_required(login_url='login')
def userpage(request, userid):
    allpost = User.objects.get(pk=userid).posts_created.order_by('-timestamp').all()
    paginator = Paginator(allpost, 10)
    page = request.GET.get('page')

    return render(request, "network/userpage.html", {
        "userdisplayed": User.objects.get(pk=userid),
        "allposts": paginator.get_page(page)
    })

@login_required(login_url='login')
def followfeed(request):
    allpost = Post.objects.filter(author__in=request.user.following.all()).order_by('-timestamp')
    paginator = Paginator(allpost, 10)
    page = request.GET.get('page')

    return render(request, "network/followfeed.html", {
        "allposts": paginator.get_page(page)
    })

def togglelike(request, postid):
    post = Post.objects.get(pk=postid)
    liked = User.objects.get(pk=request.user.pk).liked_posts

    if post not in liked.all():
        liked.add(post)
    else:
        liked.remove(post)

    return HttpResponse("done")

def togglefollow(request, userdisid):
    userToFollow = User.objects.get(pk=userdisid)

    if userToFollow not in request.user.following.all():
        request.user.following.add(userToFollow)
    else:
        request.user.following.remove(userToFollow)

    return HttpResponse('done')

@csrf_exempt
def editpost(request):
    content = request.POST.get("content")
    postid = int(request.POST.get("postid"))

    post = Post.objects.get(pk=postid)

    if post.author != request.user:
        return HttpResponse("error")

    post.content = content
    post.save(update_fields=["content"])

    return HttpResponse("done")



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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")