from django.contrib import admin
from .models import *
@admin.register(user)
class userModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "is_staff", "is_active"]

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone"]

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["title","price"]
@admin.register(Slider)
class SliderModelAdmin(admin.ModelAdmin):
    list_display = ["id","name"]

# Register your models here.
