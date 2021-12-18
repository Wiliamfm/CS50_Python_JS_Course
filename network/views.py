from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.timezone import now

import json

from .models import *


def index(request):
    return render(request, "network/index.html")

@csrf_exempt
def post(request):
    if request.method == 'POST':
        #create post
        if request.user.is_authenticated:
            user= request.user
            data= json.loads(request.body)
            text= data.get("text")
            Post.objects.create(user=user, text=text)
            return JsonResponse({"message": "post create successfully"}, status=201)
        else:
            return JsonResponse({"message": "error in the user authenticated"}, status= 500)
        #edit post
        pass
    else:
        #see posts - get
        return postPage(request, 1)

@login_required
@csrf_exempt
def editPost(request):
    if request.user.is_authenticated:
        if request.method == 'PUT':
            user= request.user
            data= json.loads(request.body)
            newText= data.get("text")
            post= Post.objects.get(id= data.get('id')) 
            if(post.user == user):
                post.text= newText
                post.date= now()
                post.save()
                return JsonResponse({"message": "success"}, status= 200)
            else:
                return JsonResponse({"message": f"This user {user.username} can't edit the post"}, status= 200)
        else:
            return JsonResponse({"message": "Diferent method of PUT"}, status= 200)
    else:
        return JsonResponse({"message": "user not loggin"}, status= 200)

@login_required
@csrf_exempt
def addLike(request, postId):
    try:
        if request.method == "PUT":
            post= Post.objects.get(pk=postId)
            post.likes.remove(request.user)
            return JsonResponse({"message": "success"}, status= 200)
        else:
            post= Post.objects.get(pk=postId)
            post.likes.add(request.user)
            return JsonResponse({"message": "success"}, status= 200)
    except Exception as e:
        return JsonResponse({"message": f"error {e}"}, status= 200)

def postPage(request, page= 1):
    try:
        posts= Post.objects.all().order_by("date")
        paginator= Paginator(posts, 10)
        pageObj= paginator.get_page(page)
        pageObjDict= {
            'previousPageNumber': pageObj.previous_page_number() if pageObj.has_previous() else -1,
            'nextPageNumber': pageObj.next_page_number() if pageObj.has_next() else -1,
            'number': pageObj.number,
            'posts': [post.asDict() for post in pageObj.object_list]#posts]
        }
        return JsonResponse(pageObjDict, status=200, safe=False)
    except Exception as e:
        print(e)
        raise Http404("Page not found!")

def getFollowsPostsPage(request, page):
    try:
        users= request.user.follows.all()
        p= []
        for u in users:
            p.append(Post.objects.filter(user= u).order_by('-date'))
        posts= []
        for ps in p:
            for psd in ps:
                posts.append(psd.asDict())
        paginator= Paginator(posts, 10)
        pageObj= paginator.get_page(page)
        pageObjDict= {
            'previousPageNumber': pageObj.previous_page_number() if pageObj.has_previous() else -1,
            'nextPageNumber': pageObj.next_page_number() if pageObj.has_next() else -1,
            'number': pageObj.number,
            'posts': pageObj.object_list 
        }
        return JsonResponse(pageObjDict, status=200, safe=False)
    except:
        raise Http404("Page not found!")

def userInfoPage(request, username, page):
    try:
        posts= Post.objects.filter(user=User.objects.get(username=username)).order_by('-date')
        paginator= Paginator(posts, 10)
        pageObj= paginator.get_page(page)
        pageObjDict= {
            'previousPageNumber': pageObj.previous_page_number() if pageObj.has_previous() else -1,
            'nextPageNumber': pageObj.next_page_number() if pageObj.has_next() else -1,
            'number': pageObj.number,
            'posts': [post.asDict() for post in pageObj.object_list]
        }
        return JsonResponse(pageObjDict, status=200, safe=False)
    except Exception as e:
        print(e)
        raise Http404("Page not found!")

def postFollow(request):
    return render(request, 'network/followingPost.html')

@login_required
def getFollowsPosts(request):        
    return getFollowsPostsPage(request, 1)

@csrf_exempt
def userInfo(request, username):
    if request.method == 'PUT':
        #follow an user
        userToFollow= User.objects.get(username=username)
        if request.user.is_authenticated:
            if request.user.isValidFollow(userToFollow.username):
                if request.user.areFollowing(userToFollow.username):
                    request.user.follows.remove(userToFollow)
                    print("areFollowing")
                    return JsonResponse({}, status=200, safe=False)
                else:
                    print("Following")
                    request.user.follows.add(userToFollow)
                return JsonResponse({}, status=200, safe=False)
            else:
                return JsonResponse({}, status=400, safe=False)
        else:
            return JsonResponse({}, status=400, safe=False)
    elif request.method == 'POST':
        #see user´s posts
        posts= Post.objects.filter(user=username)
        #return JsonResponse([post.asDict() for post in posts], status=200, safe= False)
    else:
        #GET
        user= User.objects.get(username=username)
        posts= Post.objects.filter(user=user)
        followingCount= len(user.follows.all())
        followersCount= User.objects.filter(follows__username= username).count()
        if request.user.is_authenticated:
            return render(request, 'network/userProfile.html', {
                'netUser': user,
                'posts': posts,
                'areFollowing': request.user.areFollowing(username),
                'isValidFollow': request.user.isValidFollow(username),
                'followingCount': followingCount,
                'followersCount': followersCount
            })
        return render(request, 'network/userProfile.html', {
            'netUser': user,
            'posts': posts,
            'followingCount': followingCount,
            'followersCount': followersCount
        })

@login_required
def followingInfo(request):
    #see user's posts that the current user follows
    user= User.objects.get(username= request.user.username)
    posts= Post.objects.filter(user=user.following)

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
def getPostsByUsername(request, username):
    user= User.objects.get(username=username)
    posts= Post.objects.filter(user=user)
    return JsonResponse([post.asDict() for post in posts], status=200, safe= False)