from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    # search
    path('search/<str:title>/', views.search),

    # 영화 관련
    path('', views.get_all_movies),
    path('top-rated/', views.get_top_rated_movies),
    path('top-ranked/', views.get_top_ranked_users_movies),
    path('<int:movie_pk>/', views.get_movie_detail),
    path('<int:movie_pk>/is-review/', views.isWriteReview),
    path('<int:movie_pk>/reviews/', views.get_or_create_reviews),
    path('<int:movie_pk>/reviews/<int:review_pk>/like/', views.like_review),
    path('reviews/<int:review_pk>/', views.get_or_update_or_delete_review),
    path('reviews/<int:review_pk>/comments/', views.get_or_create_comments),
    path('comments/<int:comment_pk>/', views.get_or_update_or_delete_comment),

    # user-review
    path('reviews/<str:username>/latest/', views.get_user_latest_reviews),
    
    # 평가하기
    path('<int:movie_pk>/rating/', views.get_or_update_rating),

    # user별
    path('users/<str:username>/top-rated/', views.get_user_top_rated_movies),
    path('users/<str:username>/genres/<int:genre_pk>/top-rated/', views.get_user_genre_top_rated_movies),


    # 장르별
    path('genres/', views.get_all_genres),
    path('genres/rankings/', views.get_genre_ranking_page_data),
    path('genres/rankings/<int:genre_id>/', views.update_genre_ranking_page_data),
    path('genres/<int:genre_pk>/', views.get_genre_all_movies),
    path('genres/<int:genre_pk>/datas/', views.get_genre_datas),
    path('genres/top-reviewed/', views.get_top_reviewed_genres),
    path('genres/top-ranked/', views.get_all_genre_top_ranked_users),
    path('genres/<int:genre_pk>/top-ranked/', views.get_genre_top_ranked_users),


    # collections
    path('collections/', views.get_or_create_collections),  # 전체 컬렉션
    path('users/<str:username>/collections/', views.get_user_collections),  # 한 유저의 컬렉션 전체
    path('collections/<int:collection_pk>/', views.get_or_update_or_delete_collection),  # 한 컬렉션 조회, 수정, 삭제
    path('user-collections/<int:collection_pk>/<int:movie_pk>/', views.create_or_delete_collection_movie),  # 컬렉션 내 영화 추가, 삭제
    path('user-collections/<int:collection_pk>/like/', views.like_collection),  # 컬렉션 좋아요
    
    # infinity scroll
    path('infinite-scroll/reviews/<int:pk>', views.infinite_scroll_review),

    # admin
    path('calc-genre-ranking/', views.calc_genre_ranking),
    path('init-genre-ranker/', views.init_genre_ranker),

    # insert data / admin
    path('insert-data/', views.insert_data),
]