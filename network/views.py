from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Connection
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create new post form
class NewPostForm(forms.Form):
    content = forms.CharField(label="New Post", max_length=280, required=True, widget=forms.Textarea(attrs={'class': 'form-control mb-2', 'rows': '4'}))


def index(request):
    '''
    This function renders index.html that displays 
    the new post form if the user is authenticated,
    and displays all posts from all users.
    '''
    posts = Post.objects.order_by("-timestamp").all()
    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    page_numbers_list = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)

    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "page_obj": page_obj,
        "page_numbers_list": page_numbers_list
    })


@login_required(login_url='/login')
def following_posts(request):
    '''
    This function renders index.html that displays 
    the new post form and displays all posts from the 
    users that the authenticated user follows.
    '''
    authenticated_user = request.user
    following = authenticated_user.get_following()
    posts = Post.objects.filter(creator__in=following).order_by("-timestamp")
    paginator = Paginator(posts, 2)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    page_numbers_list = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)

    return render(request, "network/index.html", {
        "following_posts_page": True,
        "form": NewPostForm(),
        "page_obj": page_obj,
        "page_numbers_list": page_numbers_list
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
    paginator = Paginator(profile_user_posts, 2)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    page_numbers_list = paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1)

    profile_user_followers = profile_user.get_followers()
    followers_number = len(profile_user_followers)
    profile_user_following = profile_user.get_following()
    following_number = len(profile_user_following)

    loggedIn_user_following = None
    if request.user.is_authenticated:
        loggedIn_user_following = request.user.get_following()

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "page_numbers_list": page_numbers_list,
        "followers_number": followers_number,
        "following_number": following_number,
        "loggedIn_user_following": loggedIn_user_following
    })


@csrf_exempt
def unfollow(request):
    # Unfollowing a user must be via DELETE request
    if request.method != "DELETE":
        return JsonResponse({"error": "DELETE request required."}, status=400)
    
    authenticated_user = request.user
    data = json.loads(request.body)
    profile_username = data.get("profile_username")
    profile_user = User.objects.get(username=profile_username)
    connection = Connection.objects.get(origin=authenticated_user, target=profile_user)
    print(connection)
    if not request.user.is_authenticated:
        return JsonResponse({"error": "There's no logged in user."}, status=400)
    if profile_user is None:
        return JsonResponse({"error": "User to unfollow not found."}, status=400)
    if connection is None:
        return JsonResponse({"error": "The connection requested to be deleted was not found."}, status=400)
    # delete the connection
    connection.delete()
    return JsonResponse({"message": f"You successfully unfollowed {profile_username}.",
                         "followers_count": len(profile_user.get_followers())
                         }, 
                         status=201)


        