from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Restaurant

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'hotel/restaurant_list.html'
    context_object_name = 'restaurants'
    paginate_by = 10

    def get_queryset(self):
        queryset = Restaurant.objects.all().order_by('title')
        
        # Sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'cost_high_to_low':
            queryset = queryset.order_by('-cost_for_two')
        elif sort_by == 'cost_low_to_high':
            queryset = queryset.order_by('cost_for_two')
        elif sort_by == 'rating_high_to_low':
            queryset = queryset.order_by('-rating')
        elif sort_by == 'rating_low_to_high':
            queryset = queryset.order_by('rating')

        # Filtering
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(location__icontains=city)
        
        food_type = self.request.GET.get('food_type')
        if food_type:
            queryset = queryset.filter(food_type=food_type)
        
        cuisine = self.request.GET.get('cuisine')
        if cuisine:
            queryset = queryset.filter(cuisines__name=cuisine)
        
        is_open = self.request.GET.get('is_open')
        if is_open:
            # Example: Assuming you have a method to check if the restaurant is open
            queryset = queryset.filter(is_open=True)
        
        min_rating = self.request.GET.get('min_rating')
        if min_rating:
            queryset = queryset.filter(rating__gte=min_rating)
        
        max_cost = self.request.GET.get('max_cost')
        if max_cost:
            queryset = queryset.filter(cost_for_two__lte=max_cost)
        
        return queryset

@method_decorator(login_required, name='dispatch')
class UserRestaurantsListView(ListView):
    model = Restaurant
    template_name = 'hotel/user_restaurants.html'
    context_object_name = 'restaurants'

    def get_queryset(self):
        user = self.request.user
        queryset = Restaurant.objects.filter(
            Q(bookmarked_by=user) | Q(visited_by=user)
        )
        return queryset

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'hotel/restaurant_detail.html'
    context_object_name = 'restaurant'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dishes'] = self.object.dishes.all()
        context['photos'] = self.object.photos.all()
        context['reviews'] = self.object.reviews.all()  # Ensure 'reviews' is properly related in your models
        return context
