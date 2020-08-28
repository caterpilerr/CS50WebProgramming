from django.contrib import admin

from .models import User, Listing, Bid, WatchlistItem

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("__str__",)


admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(WatchlistItem)
