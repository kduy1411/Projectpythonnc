from django.db import models
from django.utils.translation import gettext as _
# Create your models here
from django.contrib.auth.models import User
# 
# 
import datetime

class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name




class Drone(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    name = models.CharField(max_length=200 ,unique=True)
    
    public_day = models.DateTimeField(default=datetime.datetime.now)
    price = models.IntegerField(_("price"))
    origin_price = models.IntegerField(_("origin_price"))
    image = models.ImageField(upload_to="store/images",
                              default="store/images/default.png")
    viewed = models.IntegerField(default=0)
  
    def __str__(self):
        return self.name


class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=500, unique=False)

    def __str__(self):
        return self.username


class Client(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.CharField(max_length=250, unique=False)

    def __str__(self):
        return self.username


class UserProfileInfo(models.Model):
    # Create relationship from this class to User
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add any more attribute you want
    address = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    image = models.ImageField(
        upload_to="store/images/", default="store/images/people_default.png")

    def __str__(self):
        return self.user.username
