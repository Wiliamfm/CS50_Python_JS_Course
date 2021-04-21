from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wikis, name="wikis"),
    path("NewPage", views.newPage, name="newPage"),
    path("EditPage/<str:title>", views.editPage, name="editPage"),
    path("Random", views.randomWiki, name="randomWiki")
]
