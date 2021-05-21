from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.get_all_movies),
    path('top-rated/<int:count>/', views.get_top_rated_movies),
    path('<int:movie_pk>/', views.get_movie_detail),
    path('<int:movie_pk>/reviews/', views.get_or_create_reviews),
    path('reviews/<int:review_pk>/', views.get_or_update_or_delete_review),
    path('reviews/<int:review_pk>/like/', views.like_review),
    path('reviews/<int:review_pk>/comments/', views.get_or_create_comments),
    path('comments/<int:comment_pk>/', views.get_or_update_or_delete_comment),
    
    # 장르별
    path('genres/', views.get_all_genres),
    path('genres/<int:genre_pk>/datas/', views.get_genre_datas),
    path('genres/<int:genre_pk>/', views.get_genre_all_movies),
    path('genres/top-reviewed/', views.get_top_reviewed_genres),
    
    # infinity scroll
    path('infinite-scroll/reviews/', views.infinite_scroll_review),

    # insert data / admin
    path('TMDB/', views.get_all_movies_from_tmdb),  # insert data from TMDB
    path('seed-rating/', views.get_seed_rating),  # insert rating datas
    path('seed-review/', views.get_seed_review),  # insert review datas
    path('seed-comment/', views.get_seed_comment),  # insert comment datas
    path('count-ratings/', views.count_ratings),  # calculate distincted ratings
    path('count-reviews/', views.count_genre_reviews),  # count reviews by genres
]