from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Connection
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create new post form
class NewPostForm(forms.Form):
    content = forms.CharField(label="New Post", max_length=280, required=True, widget=forms.Textarea(attrs={'class': 'form-control mb-2', 'rows': '4'}))


def index(request):
    posts = Post.objects.order_by("-timestamp").all()
    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "posts": posts
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


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
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


@login_required(login_url='/login')
def new_post(request):
    '''This function saves a new post (coming 
    from a post request) in the database.
    '''
    if request.method == "POST":
        current_user = request.user
        new_post = Post()
        new_post.creator = current_user
        new_post.content = request.POST["content"]
        new_post.save()
        messages.success(request, 'Your post was uploaded successfully!')
        return HttpResponseRedirect(reverse("network:index"))
    else: # GET
        return HttpResponseRedirect(reverse("network:index"))


def profile(request, username):
    profile_user = User.objects.get(username=username)
    profile_user_posts = profile_user.posts.order_by("-timestamp")
    profile_user_followers = profile_user.get_followers()
    followers_number = len(profile_user_followers)
    profile_user_following = profile_user.get_following()
    following_number = len(profile_user_following)

    loggedIn_user_following = None
    if request.user.is_authenticated:
        loggedIn_user_following = request.user.get_following()

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "profile_user_posts": profile_user_posts,
        "followers_number": followers_number,
        "following_number": following_number,
        "loggedIn_user_following": loggedIn_user_following
    })