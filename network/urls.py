
from django.urls import path

from . import views

app_name = "network"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.new_post, name="new_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("Posts/Following", views.following_posts, name="following_posts"),

    # API routes
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("saveEditedPost", views.save_edited_post, name="save_edited_post"),
    path("liketoggle", views.like_toggle, name="like_toggle")
]
