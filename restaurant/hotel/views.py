from django.shortcuts import render, get_object_or_404, reverse,redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Restaurant, Review
from .forms import ReviewForm
from django.http import JsonResponse
from accounts.models import Bookmark
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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
            queryset = Restaurant.objects.annotate(
            avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        elif sort_by == 'rating_low_to_high':
            queryset = Restaurant.objects.annotate(
            avg_rating=Avg('reviews__rating')).order_by('avg_rating')

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

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_ratings = sum(review.rating for review in reviews)
            return total_ratings / len(reviews)
        return 0  # Default or handle the case where there are no reviews
    
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
