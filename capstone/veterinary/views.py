from django.http import JsonResponse
from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.contrib.auth.models import User
from . import models


# Create your views here.

from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username, first_name=first_name, last_name=last_name, email=email, password=password)
                user.save()
                client = models.UserApp(
                    user=user, type=models.UserType.objects.get(type="client"))
                client.save()
                return JsonResponse({
                    'username': client.user.username,
                    'first_name': client.user.first_name,
                    'last_name': client.user.last_name,
                    'email': client.user.email,
                    'role': client.type.type
                })
        except IntegrityError:
            return render(request, 'veterinary/register.html', {
                'error_msg': 'User already exists.'
            })
        except:
            return render(request, 'veterinary/register.html', {
                'error_msg': 'Unexpected error.'
            })
    return render(request, 'veterinary/register.html')


def login(request):
    pass


def logout(request):
    pass
