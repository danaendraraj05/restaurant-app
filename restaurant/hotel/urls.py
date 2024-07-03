# restaurant/hotel/urls.py

from django.urls import path
from .views import RestaurantListView, RestaurantDetailView, UserRestaurantsListView, ReviewCreateView, ReviewUpdateView
from .views import BookmarkToggleView
from hotel import views

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant-list'),
    path('user-restaurants/', UserRestaurantsListView.as_view(), name='user-restaurants'),
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurant/<int:pk>/add-review/', ReviewCreateView.as_view(), name='add-review'),
    path('restaurant/<int:pk>/edit-review/', ReviewUpdateView.as_view(), name='edit-review'),
    path('restaurant/<int:restaurant_id>/bookmark/', BookmarkToggleView.as_view(), name='bookmark-toggle'),
    path('my-bookmarked-restaurants/', views.my_bookmarked_restaurants, name='my-bookmarked-restaurants'),
    path('restaurant/<int:restaurant_id>/remove-bookmark/', views.remove_bookmark, name='remove-bookmark'),
]

