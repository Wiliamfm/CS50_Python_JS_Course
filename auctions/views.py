from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Auction, User, Bid, WatchList, Comment


def index(request):
    auctions= Auction.objects.filter(state=True)
    list_auctions= []
    for auction in auctions:
        auctions_bids= Bid.objects.filter(auction= auction)
        auctions_list= {'id': auction.id, 'title': auction.title, 'description': auction.description, 'category': auction.category, 'bid': auctions_bids.order_by('price').last().price, 'image':auction.image, 'user': auction.user}
        list_auctions.append(auctions_list)
    return render(request, "auctions/index.html", {
        "auctions": list_auctions,
    })

def indexF(request, category):
    auctions= Auction.objects.filter(category= category)
    list_auctions= []
    for auction in auctions:
        if auction.state:
            auctions_bids= Bid.objects.filter(auction= auction)
            auctions_list= {'id': auction.id, 'title': auction.title, 'description': auction.description, 'category': auction.category, 'bid': auctions_bids.order_by('price').last().price, 'image':auction.image, 'user': auction.user}
            list_auctions.append(auctions_list)
    return render(request, "auctions/index.html", {
        "auctions": list_auctions,
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_auction(request):
    if request.method == "POST":
        print('creating new auction')
        title= request.POST["title"]
        description= request.POST["description"]
        category= request.POST["category"]
        image= request.POST["image"]
        bid= int(request.POST["bid"])
        user= request.user
        state= True
        try:
            auction= Auction.objects.create(title= title, description= description, category= category, image= image, user= user, state= state)
            bid= Bid.objects.create(price=bid, user= user, auction= auction)
            #auction.save()
        except Exception as e:
            print(f"Error saving new Auction: {e}")
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/createAuction.html")

def auction(request, id):
    auction= Auction.objects.get(pk=id)
    order= Bid.objects.filter(auction= auction).order_by('price').last()
    comments= Comment.objects.filter(auction= auction) 
    try:        
        watchlist= WatchList.objects.filter(item=auction, user= request.user)
        if watchlist:
            a= True
        else:
            a= False
    except:
        a= False
    if request.method == "POST":
        if request.user.is_authenticated:
            bid= int(request.POST["bid"])
            if bid > order.price:
                bid= Bid.objects.create(price= bid, user= request.user, auction= auction)
                auction.save()
                order= Bid.objects.filter(auction= auction).order_by('price').last()
            else:
                return render(request, "auctions/auction.html", {
                    'message': "the bid is not greater",
                    'auction': auction,
                    'bid': order,
                    'watchlist': a,
                    'comments': comments
                })
        else:
            return HttpResponseRedirect(reverse("login"))
    return render(request, "auctions/auction.html", {
        'auction': auction,
        'bid': order,
        'watchlist': a,
        'comments': comments
    })

@login_required
def watchlist(request, auction_id):
    if request.method == 'POST':
        try:
            watchlist= WatchList.objects.filter(item=Auction.objects.get(pk=int(request.POST["auctionId"])), user= request.user)
            if watchlist:
                watchlist.delete()
            else:
                watchlist= WatchList.objects.create(item=Auction.objects.get(pk=auction_id), user= request.user)
        except:
            watchlist= WatchList.objects.create(item=Auction.objects.get(pk=auction_id), user= request.user)
        #watchlist.item.add(Auction.objects.get(pk=auction_id))
        return HttpResponseRedirect(reverse('auction', args=[auction_id]))
    else:
        user= User.objects.get(pk=request.user.id)
        return render(request, "auctions/watchlist.html", {
            'user': user
        })

@login_required
def close_auction(request, id):
    auction= Auction.objects.get(pk=id)
    if auction:
        print(request.POST["state"])
        auction.state= False
        auction.save()
        return HttpResponseRedirect(reverse('auction', args=[id]))
    else:
        print(f"Error: Couldn't find auction with id: {id}")
        return HttpResponseRedirect(reverse('auction', args=[id]))

@login_required
def add_comment(request, id):
    try:
        if request.method == 'POST':
            c= request.POST["comment"]
            comment= Comment.objects.create(user= request.user, auction= Auction.objects.get(pk=id), message= c)
        return HttpResponseRedirect(reverse('auction', args=[id]))
    except:
        return HttpResponseRedirect(reverse('auction', args=[id]))

def categories(request):
    categories= set()
    auctions= Auction.objects.all()
    for a in auctions:
        categories.add(a.category)
    return render(request, 'auctions/categories.html', {
        "categories": categories,
        "auctions": Auction.objects
    })