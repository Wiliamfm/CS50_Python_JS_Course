from django.contrib import admin
from .models import User, Auction, Bid, WatchList, Comment

# Register your models here.

class WatchListAdmin(admin.ModelAdmin):
	filter_horizontal=('item',)

admin.site.register(User)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(WatchList)#, WatchListAdmin)
admin.site.register(Comment)