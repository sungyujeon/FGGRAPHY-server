from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.get_all_movies),
    path('top-rated/<int:count>/', views.get_top_rated_movies),
    path('<int:movie_pk>/', views.get_movie_detail),
    path('<int:movie_pk>/reviews/', views.get_or_create_reviews),
    path('reviews/<int:review_pk>/', views.get_or_update_or_delete_review),
    path('reviews/<int:review_pk>/comments/', views.get_or_create_comments),
    path('comments/<int:comment_pk>/', views.get_or_update_or_delete_comment),
    

    # insert data / admin
    path('TMDB/', views.get_all_movies_from_tmdb),  # insert data from TMDB
    path('seed-rating/', views.get_seed_rating),  # insert rating datas from seed lib
    path('count-ratings/', views.count_ratings),  # caculate distincted ratings
]