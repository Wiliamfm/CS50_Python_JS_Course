from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils.timezone import now

class User(AbstractUser):
    #followers= models.ForeignKey('self', on_delete=models.SET_NULL, related_name='userfollowers', null=True)
    #following= models.ForeignKey('self', on_delete=models.SET_NULL, related_name='userfollowing', null=True)
    follows= models.ManyToManyField('self', related_name= 'followees', null= True, symmetrical= False)

    def isValidFollow(self, u):
        if self.username != u:
            return True
        else:
            return False

    def areFollowing(self, u):
        for f in self.follows.all():
            if f.username == u:
                return True
        return False

    def asDict(self):
        return {'username': self.username, 'follow': self.follows.username}
    
    def __str__(self):
        return f"{self.id} - {self.username}"

class Post(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text= models.TextField()
    date= models.DateTimeField(default= now())
    likes= models.ManyToManyField(User, related_name='likes', null=True)

    def asDict(self):
        return {'id': self.id, 'user': self.user.username, 'text': self.text, 'date': f'{self.date.day}-{self.date.month}-{self.date.year}\t{self.date.hour}:{self.date.minute}:{self.date.second}', 'likes': self.getLikes(), 'userLike': self.getUsers()}

    def getLikes(self):
        try:
            return self.likes.count()
        except:
            return 0
    
    def getUsers(self):
        return [u.username for u in self.likes.all()]

    def __str__(self):
        return f"{self.id} - {self.user.username} at {self.date}"