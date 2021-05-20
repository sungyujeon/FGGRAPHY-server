from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.get_all_movies),
    path('<int:movie_pk>', views.get_movie_detail),
    path('top-rated/<int:count>', views.get_top_rated_movies),
    

    # insert data
    path('TMDB/', views.get_all_movies_from_tmdb),  # insert data from TMDB
    path('seed-rating/', views.get_seed_rating),  # insert rating datas from seed lib
    path('count-ratings/', views.count_ratings),  # caculate distincted ratings
]