from django.contrib import admin




# Register your models here.
from .models import Category, Drone, Client, Customer, UserProfileInfo

admin.site.register(Category)
admin.site.register(Drone)
admin.site.register(Client)
admin.site.register(Customer)
admin.site.register(UserProfileInfo)
