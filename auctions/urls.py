from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchList", views.watchList, name="watchList"),
    path("<int:auction_id>/auction", views.auction, name="auction"),
    path("<int:category_id>/category", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("create_bid", views.create_bid, name="create_bid"),
    path("comments", views.comments, name="comments"),
    path("<int:auction_id>/close_auctions", views.close_auctions, name="close_auctions")
    
]
