from django.shortcuts import render, get_object_or_404, reverse,redirect
from django.views.generic import ListView, DetailView
from django.db.models import Avg,Q
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant, Review
from .forms import ReviewForm
from django.http import JsonResponse
from accounts.models import Bookmark,Visited
from django.views import View
import django_filters

class RestaurantFilter(django_filters.FilterSet):
    city = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    food_type = django_filters.CharFilter(field_name='food_type')
    cuisine = django_filters.CharFilter(field_name='cuisines__name')
    is_open = django_filters.BooleanFilter(field_name='is_open')
    min_rating = django_filters.NumberFilter(method='filter_by_min_rating')
    max_cost = django_filters.NumberFilter(method='filter_by_max_cost')

    class Meta:
        model = Restaurant 
        fields = ['city', 'food_type', 'cuisine', 'is_open', 'min_rating', 'max_cost']

    def filter_by_min_rating(self, queryset, name, value):
        try:
            value = float(value)
            return queryset.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=value)
        except ValueError:
            return queryset

    def filter_by_max_cost(self, queryset, name, value):
        try:
            value = float(value)
            return queryset.filter(cost_for_two__lte=value)
        except ValueError:
            return queryset

class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurant_list.html'
    context_object_name = 'restaurants'

    def get_queryset(self):
        queryset = Restaurant.objects.all().order_by('title')

        search_term = self.request.GET.get('search_hidden')
        print(search_term)
        if search_term:
            queryset = queryset.filter(Q(title__icontains=search_term))
        queryset = self.apply_sorting(queryset)
        queryset = self.apply_filters(queryset)
        return queryset

    def apply_sorting(self, queryset):
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'cost_high_to_low':
            return queryset.order_by('-cost_for_two')
        elif sort_by == 'cost_low_to_high':
            return queryset.order_by('cost_for_two')
        elif sort_by in ['rating_high_to_low', 'rating_low_to_high']:
            return self.sort_by_rating(queryset, sort_by)
        return queryset

    def sort_by_rating(self, queryset, sort_by):
        annotation = '-avg_rating' if sort_by == 'rating_high_to_low' else 'avg_rating'
        return queryset.annotate(avg_rating=Avg('reviews__rating')).order_by(annotation)
    
    def apply_filters(self, queryset):
        filterset = RestaurantFilter(self.request.GET, queryset=queryset)
        return filterset.qs

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'hotel/restaurant_detail.html'
    context_object_name = 'restaurant'

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_ratings = sum(review.rating for review in reviews)
            return total_ratings / len(reviews)
        return 0 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dishes'] = self.object.dishes.all()
        context['photos'] = self.object.photos.all()
        context['reviews'] = self.object.reviews.all()
        if self.request.user.is_authenticated:
            try:
                context['user_review'] = Review.objects.get(user=self.request.user, restaurant=self.object)
            except Review.DoesNotExist:
                context['user_review'] = None
        if self.request.user.is_authenticated:
            context['bookmarked_by_user'] = Bookmark.objects.filter(user=self.request.user, restaurant=self.object).exists()
            context['visited_by_user'] = Visited.objects.filter(user=self.request.user, restaurant=self.object).exists()
        return context

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'hotel/review_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.restaurant = get_object_or_404(Restaurant, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('restaurant-detail', args=[str(self.object.restaurant.pk)])

class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'hotel/review_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Review, restaurant_id=self.kwargs['pk'], user=self.request.user)

    def get_success_url(self):
        return reverse('restaurant-detail', args=[str(self.object.restaurant.pk)])
    
class BookmarkToggleView(View):
    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        user = request.user

        # Check if the user has already bookmarked this restaurant
        bookmark, created = Bookmark.objects.get_or_create(user=user, restaurant=restaurant)

        if not created:
            # Bookmark already exists, delete it (unbookmark)
            bookmark.delete()
            action = 'remove'
        else:
            # Bookmark doesn't exist, create it (bookmark)
            action = 'add'

        return JsonResponse({'action': action})

@login_required
def my_bookmarked_restaurants(request):
    user = request.user
    bookmarks = Bookmark.objects.filter(user=user)
    bookmarked_restaurants = [bookmark.restaurant for bookmark in bookmarks]
    
    context = {
        'bookmarked_restaurants': bookmarked_restaurants
    }
    return render(request, 'hotel/bookmarked_restaurants.html', context)

@login_required
def remove_bookmark(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    bookmark = Bookmark.objects.filter(user=request.user, restaurant=restaurant).first()
    
    if bookmark:
        bookmark.delete()

    return redirect('my-bookmarked-restaurants')

# hotel/views.py

class VisitedToggleView(View):
    def post(self, request, restaurant_id):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        user = request.user

        # Check if the user has already marked this restaurant as visited
        visited, created = Visited.objects.get_or_create(user=user, restaurant=restaurant)

        if not created:
            # Visited entry already exists, delete it (unmark as visited)
            visited.delete()
            action = 'remove'
        else:
            # Visited entry doesn't exist, create it (mark as visited)
            action = 'add'

        return JsonResponse({'action': action})

@login_required
def my_visited_restaurants(request):
    user = request.user
    visited = Visited.objects.filter(user=user)
    visited_restaurants = [visit.restaurant for visit in visited]
    
    context = {
        'visited_restaurants': visited_restaurants
    }
    return render(request, 'hotel/visited_restaurants.html', context)

@login_required
def remove_visited(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    visited = Visited.objects.filter(user=request.user, restaurant=restaurant).first()
    
    if visited:
        visited.delete()

    return redirect('my-visited-restaurants')

