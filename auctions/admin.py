from django.contrib import admin
from  .models import *



# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction)
admin.site.register(WatchList)
admin.site.register(Comments)
admin.site.register(Bid)


