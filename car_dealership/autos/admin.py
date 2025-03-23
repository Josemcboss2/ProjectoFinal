from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Car, Article, ContactMessage

admin.site.register(Car)
admin.site.register(Article)
admin.site.register(ContactMessage)