from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE


class User(AbstractUser):
    pass

class Auction(models.Model):
    title= models.CharField(max_length= 64)
    description= models.CharField(max_length= 64)
    category= models.CharField(max_length= 64)
    #bid= models.PositiveBigIntegerField()
    image= models.TextField()
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='auctions')
    state= models.BooleanField()
    
    def __str__(self):
        return f"{self.id}: {self.title}"

class Bid(models.Model):
    price= models.PositiveBigIntegerField()
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    auction= models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.id}: {self.user.username}"

class WatchList(models.Model):
    #item= models.ManyToManyField(Auction)
    item= models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watchlist")
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='watchlist')

    def __str__(self):
        return f"{self.id}: {self.item} by {self.user}"

class Comment(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    auction= models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    message= models.CharField(max_length=200)
    date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.user} in {self.auction.title}"