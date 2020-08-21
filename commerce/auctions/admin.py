from django.contrib import admin

from .models import User, Listing, Bid

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

admin.site.register(User, UserAdmin)