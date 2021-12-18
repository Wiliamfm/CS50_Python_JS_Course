
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("post", views.post, name="post"),
    path("post/like/<int:postId>", views.addLike, name="post"),
    path("post/<int:page>", views.postPage, name="postPage"),
    path("post/follows", views.postFollow, name="postFollow"),
    path("post/getFollowsPosts", views.getFollowsPosts, name="getFollowsPosts"),
    path("post/getFollowsPosts/<int:page>", views.getFollowsPostsPage, name="getFollowsPostsPage"),
    path("user/post", views.editPost, name="editPost"),
    path("user/<str:username>", views.userInfo, name="userInfo"),
    path("user/<str:username>/<int:page>", views.userInfoPage, name="userInfoPage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts/<str:username>", views.getPostsByUsername, name="getPostsByUsername")
]
