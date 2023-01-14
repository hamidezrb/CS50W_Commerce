from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length=64)
    createdate = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.title

class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(blank = True,max_length=500)
    starting_bid = models.DecimalField(decimal_places=2,max_digits=10)
    image_url = models.URLField(blank=True, null=True)
    enabled = models.BooleanField(default = True)
    createdate = models.DateTimeField(auto_now_add = True)
    category = models.ForeignKey(Category,blank=True, null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"title : {self.title} , bid : {self.starting_bid}"

    
class WatchList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"username : {self.user.username} , auction : {self.auction.title}"

class Comments(models.Model):
    text = models.CharField(max_length=500)
    createdate = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"username : {self.user.username} , auction : {self.auction.title}"

    
class Bid(models.Model):
    price = models.DecimalField(decimal_places=2,max_digits=10)
    createdate = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction,on_delete=models.CASCADE)
    
  
    def __str__(self):
        return str(self.price)
 
    
    

    
    
    
    