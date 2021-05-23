from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    # 영화 관련
    path('', views.get_all_movies),
    path('top-rated/', views.get_top_rated_movies),
    path('<int:movie_pk>/', views.get_movie_detail),
    path('<int:movie_pk>/reviews/', views.get_or_create_reviews),
    path('reviews/<int:review_pk>/', views.get_or_update_or_delete_review),
    path('<int:movie_pk>/reviews/<int:review_pk>/like/', views.like_review),
    path('reviews/<int:review_pk>/comments/', views.get_or_create_comments),
    path('comments/<int:comment_pk>/', views.get_or_update_or_delete_comment),
    
    # 평가하기
    path('<int:movie_pk>/rating/', views.set_rating),

    # user별
    path('users/<str:username>/top-rated/', views.get_user_top_rated_movies),
    path('users/<str:username>/genres/<int:genre_pk>/top-rated/', views.get_user_genre_top_rated_movies),

    # 장르별
    path('genres/', views.get_all_genres),
    path('genres/<int:genre_pk>/', views.get_genre_all_movies),
    path('genres/<int:genre_pk>/datas/', views.get_genre_datas),
    path('genres/top-reviewed/', views.get_top_reviewed_genres),
    path('genres/top-ranked/', views.get_all_genre_top_ranked_users),

    # collections
    path('collections/', views.get_or_create_collections),
    path('collections/<int:collection_pk>/', views.get_or_update_or_delete_collection),
    path('user-collections/<int:collection_pk>/<int:movie_pk>/', views.create_or_delete_collection_movie),
    path('user-collections/<int:collection_pk>/like/', views.like_collection),
    
    # infinity scroll
    # 어떤 영화인지 pk값이 필요해서 추가함
    path('infinite-scroll/reviews/<int:pk>', views.infinite_scroll_review),

    # admin
    path('calc-genre-ranking/', views.calc_genre_ranking),

    # insert data / admin
    path('insert-data/', views.insert_data),
]