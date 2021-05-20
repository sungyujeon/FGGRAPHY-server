from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('TMDB/', views.get_all_movies_from_tmdb, name='getMovies'),  # insert data from TMDB
    path('seed-rating/', views.get_seed_rating, name='movieSeedRating'),
]