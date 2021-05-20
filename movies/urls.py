from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.get_all_movies_from_tmdb, name="getMovies"),
]