from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import *

class AuctionForm(forms.Form):
    title = forms.CharField(
        max_length=64,
         widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "form-control col-12"}
        ))
    description = forms.CharField(
        max_length=500,
         widget=forms.TextInput(
            attrs={"placeholder": "description", "class": "form-control col-12"}
        ))
    starting_bid = forms.DecimalField(
        decimal_places=2,
        max_digits=10,
        widget=forms.TextInput(
            attrs={"placeholder": "starting bid", "class": "form-control col-12"}
        ))
    image_url = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "image url", "class": "form-control col-12"}
        )
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control col-12'})
    )
    
    
def index(request):
    auctions = Auction.objects.filter(enabled = True).order_by("-createdate")
    return render(request, "auctions/index.html",{
        "auctions" : auctions 
    })

def auction(request,auction_id):
    winner = False
    watchList_status = False
    auction = Auction.objects.filter(id = auction_id).first()
    if  auction is None : 
        message = "auction is not found"
        return render(request, "auctions/Error.html", {
              "message" : message
          })
        
    comments = Comments.objects.filter(auction = auction).order_by('-createdate')
    highest_Bid = Bid.objects.filter(auction = auction).order_by('-price').first()
            
    if request.user.is_authenticated:  
        if highest_Bid is not None and auction.enabled == False:
                if  highest_Bid.user.id == request.user.id:
                    winner = True  
                    
        user = User.objects.get(id = request.user.id) 
        watchList = WatchList.objects.filter(auction = auction , user = user).first()   
        if watchList is None:
            watchList_status =True
    
    
    return render(request, "auctions/auction.html",{
        "auction" : auction,
        "watchList_status" : watchList_status ,
        "winner" : winner,
        "highest_Bid" : highest_Bid.price if highest_Bid is not None else auction.starting_bid,
        "comments" : comments
    })
 
@login_required(login_url='/login')
def comments(request):
    if request.method == "POST":
        auction_id = request.POST["auction_id"]
        comment = request.POST["comment"]
        if comment is None:
            message = "comment is rquired"
            return render(request, "auctions/Error.html", {
              "message" : message
            })
            
        auction = Auction.objects.filter(id = auction_id).first()
        if auction is None:
            message = "auction is not found"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
       
        user = User.objects.get(id = request.user.id)
        #  add comments 
        watchlist = Comments(
                text = comment,
                user = user,
                auction = auction
            )
        watchlist.save()
           
        return HttpResponseRedirect(reverse("auction",kwargs={"auction_id" : auction_id}))
    
    else:
        message = "try again to add Comment"
        return render(request, "auctions/Error.html", {
              "message" : message
          })
        
@login_required(login_url='/login')
def close_auctions(request,auction_id):
    if request.method == "POST":
        auction = Auction.objects.filter(id = auction_id).first()
        if auction is None:
            message = "auction is not found"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
        if  auction.user.id != request.user.id:
            message = "you are not allowed to close"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
            
        auction.enabled = False
        auction.save()
           
        return HttpResponseRedirect(reverse("index"))
    
    else:
        message = "try again to close auctions"
        return render(request, "auctions/Error.html", {
              "message" : message
          })
        
        

@login_required(login_url='/login')
def watchList(request):
    if request.method == "POST":
        auction_id = request.POST["auction_id"]
        watchList_status = bool(eval(request.POST["watchList_status"]))
        auction = Auction.objects.filter(id = auction_id).first()
        if auction is None:
            message = "auction is not found"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
        if auction.enabled == False:
            message = "auction is closed"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
       
        user = User.objects.get(id = request.user.id)
        #  add watchList 
        if watchList_status == True :
            watchlist = WatchList(
                    user = user,
                    auction = auction
                )
            watchlist.save()
            
        #  remove watchList 
        else:
            watchList = WatchList.objects.filter(user = user,
                auction = auction).first()
            watchList.delete()
           
        return HttpResponseRedirect(reverse("auction",kwargs={"auction_id" : auction_id}))
    else:
         return render(request, "auctions/watchList.html", {
        "watchlist_items": WatchList.objects.filter(user = request.user.id)
    })
    
def categories(request):
    return render(request, "auctions/categories.html",{
        "categories" : Category.objects.all()
    })

def category(request,category_id):
    categories = Category.objects.all()
    category = categories.filter(id = int(category_id)).first()
    if  category is None:
        message = "category is not found"
        return render(request, "auctions/Error.html", {
          "message" : message
      })
    auctions = Auction.objects.filter(category = category, enabled=True)
    return render(request, "auctions/index.html", {
            "auctions": auctions
        })
   
def create_listing(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            image_url = form.cleaned_data["image_url"]
            starting_bid = form.cleaned_data["starting_bid"]
            # Save a record
            user = User.objects.get(id = request.user.id)
            auction = Auction(
                user = user,
                title = title,
                description = description,
                category = category,
                image_url = image_url,
                starting_bid = starting_bid
            )
            auction.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
          return render(request, "auctions/create.html", {
              "form" : AuctionForm()
          })
      

@login_required(login_url='/login')
def create_bid(request):
    if request.method == "POST":
        price = int(request.POST["price"])
        auction_id = request.POST["auction_id"]
        
        if  price <= 0:
            message = "Bid price must be greater than 0"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
      
        
        auction = Auction.objects.filter(id = auction_id).first()
        if auction is None:
            message = "auction is not found"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
        if auction.enabled == False:
            message = "auction is closed"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
        
          
        highest_Bid = Bid.objects.filter(auction = auction_id).order_by('-price').first()
        if highest_Bid is not None and  price <= highest_Bid.price:
            message = f"your bid must be greater than {highest_Bid.price}"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
        elif(price < auction.starting_bid):
            message = f"your bid must be equal or greater than {auction.starting_bid}"
            return render(request, "auctions/Error.html", {
              "message" : message
          })
        # add new Bid
        user = User.objects.get(id = request.user.id)
        new_bid = Bid(price = price, user = user, auction = auction)
        new_bid.save()
        return HttpResponseRedirect(reverse("auction",kwargs={"auction_id" : auction_id}))

    else:
        message = "add your Bid again"
        return render(request, "auctions/Error.html", {
              "message" : message
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
    