from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from movies.recommendations import MovieRecommender
from movies.models import *
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch movies with 1+ ratings for the current user
        user_ratings = MovieRating.objects.filter(userId=self.request.user.id, rating__gte=1).order_by('-rating')
        movies=[]
        for rating in user_ratings:
            movies.append(rating.movieId)
        movies=movies[:10]
        movies_r = movies[::-1]
        rated_movies = Cinema.objects.filter(id__in=movies_r)
        rated_movie = Cinema.objects.filter(id__in=movies_r)

        # Calculate the average rating for each rated movie
        for movie in rated_movies:
            average_rating = MovieRating.objects.filter(movieId=movie.id).aggregate(Avg('rating'))['rating__avg'] or 0
            movie.average_rating = average_rating
        print(rated_movies)
        # Add the rated movies to the context
        context['rated_movies'] = rated_movies
        # Fetch all unique genres from the rated movies
        all_genres = set()
        for movie in rated_movie:
            genres = movie.genres.split(',')  # Assuming genres are stored as a comma-separated string
            for genre in genres:
                all_genres.add(genre.strip())  # Add the genre to the set (to avoid duplicates)

        movies=Cinema.objects.all()
        user_ratings = MovieRating.objects.all()
        context['user_ratings'] = user_ratings
        return context

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
# Register view
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        try:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
        except:
            return render(request, 'register.html', {'error': 'Username already taken'})

    return render(request, 'register.html')
@login_required
def home_view(request):
    # Fetch movies with 4+ ratings
    user_ratings = MovieRating.objects.filter(userId=request.user.id, rating__gte=1)
    print("abc")
    print(user_ratings)
    rated_movies = Cinema.objects.filter(id__in=[rating.movieId for rating in user_ratings])

    return render(request, 'home.html', {'rated_movies': rated_movies,'user_ratings':user_ratings})

def logout_view(request):
    logout(request)
    return redirect('logins')


from django.shortcuts import render, get_object_or_404
from movies.models import *  # Make sure to import your Movie model


# Import the recommender class
from movies.recommendations import MovieRecommender

def movie_detail(request, movie_id):
    movie = get_object_or_404(Cinema, id=movie_id)
    genres = movie.genres.split(',') if movie.genres else []
    #user_rating = MovieRating.objects.
    # Get the current user's rating, if it exists
    user_rating = MovieRating.objects.filter(userId=request.user.id, movieId=movie_id).first()
    user_rating_value = user_rating.rating if user_rating else 0
    average_rating = MovieRating.objects.filter(movieId=movie_id).aggregate(Avg('rating'))['rating__avg'] or 0
    # Instantiate the recommender
    recommender = MovieRecommender()
    print("Movie is",movie_id)
    user_id=request.user.id
    # Get content-based recommendations
    
    recommendations = recommender.recommend_movies(movie_id, user_id)
    # Assuming you have a model named Cinema
    cinema_objects = Cinema.objects.filter(id__in=recommendations)

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'genres': genres,
        'average_rating': average_rating,
        'user_rating': user_rating_value,
        'recommendations': cinema_objects,
        
        #'collaborative_recommendations': collaborative_recommendation_movies
    })

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json
from datetime import datetime
import csv
@csrf_exempt
def rate_movie(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('userId')
        movie_id = data.get('movieId')
        rating_value = data.get('rating')
        
        movie = get_object_or_404(Cinema, tmdbId=movie_id)
        rating, created = MovieRating.objects.get_or_create(userId=user_id, movieId=movie.id)
        rating.rating = rating_value
        rating.timestamp=datetime.now()
        rating.save()
        ratings_list = MovieRating.objects.filter(movieId=movie.id,userId=user_id).first() # Order by creation date (most recent first)
        with open('staticfiles/filtered_ratings.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
    
            # Add a row of data to the CSV
            writer.writerow([ratings_list.id, ratings_list.userId, ratings_list.movieId, ratings_list.rating, ratings_list.timestamp])

        print(ratings_list.id)
        print(ratings_list.userId)
        print(ratings_list.movieId)
        print(ratings_list.rating)
        print(ratings_list.timestamp)
        return JsonResponse({'success': True, 'rating': rating_value})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
