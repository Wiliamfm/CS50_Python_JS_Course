from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("/<str:category>", views.indexF, name="indexFilter"),
    path("categories", views.categories, name="categories"),
    #path("accounts/login/", auth_views.LoginView.as_view(), name="loginRedirect"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createAuction", views.create_auction, name="create_auction"),
    path("Auction/<int:id>", views.auction, name="auction"),
    path("WatchList/<int:auction_id>", views.watchlist, name="watchlist"),
    path("closeAuction/<int:id>", views.close_auction, name="close_auction"),
    path("addComment/<int:id>", views.add_comment, name="add_comment")
]
