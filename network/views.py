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
    
    # Verify current user is logged in
    authenticated_user = request.user
    if not request.user.is_authenticated:
        return JsonResponse({"error": "There's no logged in user."}, status=400)
    
    # Verify 'profile_username' field is in the request body
    data = json.loads(request.body)
    profile_username = data.get("profile_username")
    if profile_username is None:
        return JsonResponse({"error": "'profile_username' not found in request data."}, status=400)
    
    # Verify the username matches a User object
    try:
        profile_user = User.objects.get(username=profile_username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Username didn't match any User."}, status=400)
    
    # Verify that the connection between the users exists, if so detele it
    try:
        connection = Connection.objects.get(origin=authenticated_user, target=profile_user)
        if connection.delete()[0]: # != 0
            return JsonResponse({"message": f"You successfully unfollowed {profile_username}.",
                                "followers_count": len(profile_user.get_followers())
                                }, 
                                status=201)
        else:
            return JsonResponse({"error": "An error occured while deleting the connection."}, status=400)
    except Connection.DoesNotExist:
        return JsonResponse({"error": "The connection requested to be deleted was not found."}, status=400)


@csrf_exempt
def follow(request):
    # following a user must be via POST request
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Verify current user is logged in
    authenticated_user = request.user
    if not request.user.is_authenticated:
        return JsonResponse({"error": "There's no logged in user."}, status=400)
    
    # Verify 'profile_username' field is in the request body
    data = json.loads(request.body)
    profile_username = data.get("profile_username")
    if profile_username is None:
        return JsonResponse({"error": "'profile_username' not found in request body."}, status=400)
    
    # Verify the username matches a User object
    try:
        profile_user = User.objects.get(username=profile_username)
    except User.DoesNotExist:
        return JsonResponse({"error": "Username didn't match any User."}, status=400)
    
    # Check if the connection already exists. If not, add the new connection to the Connection model
    try:
        connection = Connection.objects.get(origin=authenticated_user, target=profile_user)
    except Connection.DoesNotExist:
        new_connection = Connection()
        new_connection.origin = authenticated_user
        new_connection.target = profile_user
        new_connection.save()
        return JsonResponse({"message": f"You are now following {profile_username}!",
                            "followers_count": len(profile_user.get_followers())}, 
                            status=201)
    return JsonResponse({"error": f"You are already following {profile_username}!"})


@csrf_exempt
@login_required(login_url='/login')
def save_edited_post(request):
    # Editing a post must be via PUT request
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    data = json.loads(request.body)
    post_id = data.get("post_id")

    # Verify that the post_id is in the request body
    if post_id is None:
        return JsonResponse({"error":" 'post_id' not found in the request body."}, status=400)

    # Verify that the post id matches a Post object
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post id did not match any Post object."}, status=400)
    
    # Make sure that the authenticated user is the post creator, so has the rights to edit the post.
    if request.user != post.creator:
        return JsonResponse({"error": "The authenticated user is not the creator of the post requested to be edited."})
    
    new_post_content = data.get("text_area_content")
    # Verify that the text_area_content is in the request body
    if new_post_content is None:
        return JsonResponse({"error":" 'text_area_content' not found in the request body."}, status=400)
    else:
        new_post_content = new_post_content.strip()
        # Verify that the text area content is not empty
        if new_post_content == "":
            return JsonResponse({"error":" The post content can not be empty!"}, status=400)
        # Verify that the text area content does not exceed 280 characters
        if len(new_post_content) > 280:
            return JsonResponse({"error":" You exceeded the maximum character length that is 280."}, status=400)

    post.content = new_post_content
    post.save()
    return JsonResponse({"message": "The post was edited successfully."}, status=201)


@csrf_exempt
@login_required(login_url='/login')
def like_toggle(request):
    # Liking a post must be via PUT request
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)
    
    data = json.loads(request.body)
    post_id = data.get("post_id")

    # Verify that the post_id is in the request body
    if post_id is None:
        return JsonResponse({"error": " 'post_id' not found in the request body. "}, status=400)
    
    # Verify that the post id matches a Post object
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post id did not match any Post object."}, status=400)
    
    # Unlike the post
    if request.user in post.likers.all():
        post.likers.remove(request.user)
        post.save()
        return JsonResponse({"message": "You unliked the post!",
                             "like": False,
                             "likes_count": post.likers.count()}, 
                             status=201)
    # like the post
    else:
        post.likers.add(request.user)
        post.save()
        return JsonResponse({"message": "You liked the post!",
                             "like": True,
                             "likes_count": post.likers.count()}, 
                             status=201)
