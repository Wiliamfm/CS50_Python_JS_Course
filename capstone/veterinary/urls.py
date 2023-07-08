from django.urls import path
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(
        template_name='veterinary/login.html',
        next_page='veterinary/Make-Appointment.html'),
        name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='veterianry/logout.html'), name='logout'),
]
