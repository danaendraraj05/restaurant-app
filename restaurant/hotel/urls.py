# restaurant/hotel/urls.py

from django.urls import path
from .views import RestaurantListView, RestaurantDetailView, UserRestaurantsListView

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant-list'),
    path('user-restaurants/', UserRestaurantsListView.as_view(), name='user-restaurants'),
    path('restaurant/<int:pk>/', RestaurantDetailView.as_view(), name='restaurant-detail'),
]
