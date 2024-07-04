# restaurant/hotel/urls.py

from django.urls import path
from .views import RestaurantListView, RestaurantDetailView, ReviewCreateView, ReviewUpdateView
from .views import BookmarkToggleView
from hotel import views
from .views import VisitedToggleView, my_visited_restaurants, remove_visited

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant-list'),
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
    path('restaurant/<int:pk>/add-review/', ReviewCreateView.as_view(), name='add-review'),
    path('restaurant/<int:pk>/edit-review/', ReviewUpdateView.as_view(), name='edit-review'),
    path('restaurant/<int:restaurant_id>/bookmark/', BookmarkToggleView.as_view(), name='bookmark-toggle'),
    path('my-bookmarked-restaurants/', views.my_bookmarked_restaurants, name='my-bookmarked-restaurants'),
    path('restaurant/<int:restaurant_id>/remove-bookmark/', views.remove_bookmark, name='remove-bookmark'),
    path('restaurant/<int:restaurant_id>/visited_toggle/', VisitedToggleView.as_view(), name='visited-toggle'),
    path('my_visited_restaurants/', my_visited_restaurants, name='my-visited-restaurants'),
    path('restaurant/<int:restaurant_id>/remove_visited/', remove_visited, name='remove-visited'),
]

