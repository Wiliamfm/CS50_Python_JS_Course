from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("Wiki/<str:title>", views.wikis, name="wikis")
]
