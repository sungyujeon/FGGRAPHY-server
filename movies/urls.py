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
    path('genres/top-ranked/', views.get_all_genre_top_ranked_users),

    # collections
    path('collections/', views.get_or_create_collections),
    path('collections/<int:collection_pk>/', views.get_or_update_or_delete_collection),
    path('user-collections/<int:collection_pk>/<int:movie_pk>/', views.create_or_delete_collection_movie),
    
    # infinity scroll
    path('infinite-scroll/reviews/', views.infinite_scroll_review),

    # admin
    path('calc-genre-ranking/', views.calc_genre_ranking),

    # insert data / admin
    path('TMDB/', views.get_all_movies_from_tmdb),  # insert data from TMDB
    path('seed-rating/', views.get_seed_rating),  # insert rating datas
    path('seed-review/', views.get_seed_review),  # insert review datas
    path('seed-comment/', views.get_seed_comment),  # insert comment datas
    path('count-ratings/', views.count_ratings),  # calculate distincted ratings
    path('count-reviews/', views.count_genre_reviews),  # count reviews by genres
    path('count-comments/', views.count_genre_comments),  # count comments by genres
]