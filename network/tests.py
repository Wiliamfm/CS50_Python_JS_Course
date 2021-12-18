from django.test import TestCase
from .models import *
import datetime

# Create your tests here.

class NetworkTestCases (TestCase):

  def setUp(self):

    #Create users
    u= User.objects.create(username= 'user1')
    u2= User.objects.create(username= 'user2')
    u3= User.objects.create(username= 'user3')

    #Create posts
    p= Post.objects.create(id= 1, user= u, text= 'Post1', date= datetime.datetime.now())
    p1= Post.objects.create(id= 2, user= u2, text= 'Post2', date= datetime.datetime.now())
    p2= Post.objects.create(id= 3, user= u2, text= 'Post3', date= datetime.datetime.now())
    p3= Post.objects.create(id= 4, user= u3, text= 'Post1', date= datetime.datetime.now())

  def testAddLike(self):
    #Test 1
    u= User.objects.get(username= 'user1')
    u.likes.add(Post.objects.get(id=1))
    self.assertEqual(u.likes.count(), 1)

  def testAddFollower(self):
    #Test 2
    u= User.objects.get(username='user1')
    u2= User.objects.get(username='user2')
    u.userfollowers.add(u2)
    self.assertEqual(u.userfollowers.count(), 1)
  
  def testAddFollowing(self):
    #Test 3
    u= User.objects.get(username='user1')
    u2= User.objects.get(username='user2')
    u.userfollowing.add(u2)
    self.assertEqual(u.userfollowing.count(), 1)

  def testAddItselfAsFollower(self):
    #Test 4
    u= User.objects.get(username='user1')
    self.assertFalse(u.isValidFollow(u))
  
  def testCountPost(self):
    #Test 5
    u= User.objects.get(username= 'user1')
    u2= User.objects.get(username= 'user2')
    self.assertEqual(u.posts.count(), 1)
    self.assertEqual(u2.posts.count(), 2)
  
  def testcreatePost(self):
    #Test 6
    u= User.objects.get(username= 'user1')
    u.posts.add(Post.objects.create(user=u, text='post'))
    self.assertEqual(u.posts.count(), 2)

  def testDeletePost(self):
    #Test 7
    u= User.objects.get(username= 'user1')
    u.posts.get(id=1).delete()
    self.assertEqual(u.posts.count(), 0)