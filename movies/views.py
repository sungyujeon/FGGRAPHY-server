# tmp libraries
from pprint import pprint
# end tmp libraries

from django.contrib.auth import get_user_model
User = get_user_model()

from .modules import TmdbMovie, Ranking
from .models import Movie, Movie_User_Rating, Movie_User_Genre_Rating, Review, Comment, Genre, Genre_User, Collection
from .serializers import MovieListSerializer, MovieSerializer, ReviewListSerializer, ReviewSerializer, CommentListSerializer, CommentSerializer, GenreListSerializer, GenreSerializer, GenreUserListSerializer, CollectionListSerializer, CollectionSerializer

from django.core.paginator import Paginator
from django.db.models import Count, Sum
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse
from django_seed import Seed

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes

import os
import random
import requests
from dotenv import load_dotenv, dotenv_values

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_all_movies(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])   
def get_movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_top_rated_movies(request):
    movie_count = int(request.GET.get('movie_count'))
    movies = Movie.objects.all().order_by('-rating_average')[:movie_count]
    serializer = MovieListSerializer(list(movies), many=True)

    return Response(serializer.data)


# review ======================================================================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def get_or_create_reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':  # 전체 review 조회 
        reviews = movie.review_set.all()
        serializers = ReviewListSerializer(list(reviews), many=True)

        return Response(serializers.data)
    elif request.method == 'POST':  # review 생성
        serializer = ReviewListSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # test code / request.user가 현재 존재하지 않으므로 2번 user로 임시 대체
            # serializer.save(user=request.user, movie=movie)
            user = get_object_or_404(User, pk=2)
            review = serializer.save(user=user, movie=movie)

            # review 생성 시 point 증가
            ranking = Ranking()
            ranking.increase_review_point(review)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def get_or_update_or_delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':  # 단일 review 조회 
        serializers = ReviewSerializer(review)

        return Response(serializers.data)
    elif request.method == 'PUT':  # review 수정
        serializer = ReviewListSerializer(review, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':  # review 삭제
        review.delete()

        # review 생성 시 point 증가
        ranking = Ranking()
        ranking.decrease_review_point(review)

        data = {
            'success': True,
            'message': f'{review_pk}번 리뷰 삭제',
        }

        return Response(data, status=status.HTTP_200_OK)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)

# review like
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def like_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    ranking = Ranking()
    like_status = False
    try:
        # if review.like_users.filter(pk=request.user.pk).exists(): # 좋아요 취소
        if review.like_users.filter(pk=5).exists():  # test code(request.user 없음)
            # review.like_users.remove(request.user)
            user = get_object_or_404(User, pk=5)
            review.like_users.remove(user)
            like_status = False

            # review_like 포인트--
            ranking.decrease_review_like_point(review)
        else: # 좋아요 누름
            # review.like_users.add(request.user)
            user = get_object_or_404(User, pk=5)
            review.like_users.add(user)
            like_status = True

            # review_like 포인트++
            ranking.increase_review_like_point(review)
        
        data = {
            'success': True,
            'like_status': like_status,
        }
    except:
        return JsonResponse({ 'success': False })
    
    return JsonResponse(data)


# comment ======================================================================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def get_or_create_comments(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':  # 전체 comments 조회 
        comments = review.comment_set.all()
        serializers = CommentListSerializer(list(comments), many=True)

        return Response(serializers.data)
    elif request.method == 'POST':  # comment 생성
        serializer = CommentListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save(user=request.user, review=review)
            
            # test
            user = get_object_or_404(User, pk=1)
            serializer.save(user=user, review=review)

            # comment 받은 사람 point++
            ranking = Ranking()
            ranking.increase_comment_point(review)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def get_or_update_or_delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'GET':  # 단일 comment 조회 
        serializers = CommentSerializer(comment)

        return Response(serializers.data)
    elif request.method == 'PUT':  # comment 수정
        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':  # comment 삭제
        comment.delete()

        # comment 삭제 시 point--
        review = get_object_or_404(Review, pk=comment.review_id)
        ranking = Ranking()
        ranking.decrease_comment_point(review)

        data = {
            'success': True,
            'message': f'{comment_pk}번 댓글 삭제',
        }

        return Response(data, status=status.HTTP_200_OK)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)


# genre별 영화 ======================================================================
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_all_genres(request):  # 전체 장르 정보
    genres = get_list_or_404(Genre)
    serializer = GenreListSerializer(genres, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_genre_datas(request, genre_pk):  # 개별 장르 정보
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializer = GenreSerializer(genre)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_genre_all_movies(request, genre_pk):  # 개별 장르의 모든 영화 정보
    genre = get_object_or_404(Genre, pk=genre_pk)
    movies = genre.movies.all()
    serializer = MovieListSerializer(list(movies), many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_top_reviewed_genres(request):  # 장르별 리뷰순
    genres = Genre.objects.all().order_by('-total_review_count')
    serializer = GenreListSerializer(genres, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_all_genre_top_ranked_users(request):
    ranker_nums = int(request.GET.get('ranker_nums'))
    genre_ids = [12, 14, 16, 18, 27, 28, 35, 36, 37, 53, 80, 99, 878, 9648, 10402, 10749, 10751, 10752]
    
    res = {}   
    for genre_id in genre_ids:
        genre_users = Genre_User.objects.filter(genre_id=genre_id).order_by('-point')[:ranker_nums]
        serializer = GenreUserListSerializer(list(genre_users), many=True)
        genre_id = serializer.data[0].get('genre')
        res[genre_id] = serializer.data

    return Response(res)


# collections ====================================================================================
@api_view(['GET', 'POST'])
@authentication_classes([])
@permission_classes([])
def get_or_create_collections(request):
    if request.method == 'GET':  # 전체 collections 조회 
        collections = get_list_or_404(Collection)
        serializers = ReviewListSerializer(collections, many=True)

        return Response(serializers.data)
    elif request.method == 'POST':  # collection 생성
        serializer = CollectionSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            # test code / request.user가 현재 존재하지 않으므로 1번 user로 임시 대체
            # user = get_object_or_404(User, pk=request.user.id)
            user = get_object_or_404(User, pk=1)
            collection = serializer.save(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def get_or_update_or_delete_collection(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    if request.method == 'GET':  # 단일 collection 조회 
        serializer = CollectionSerializer(collection)

        return Response(serializer.data)
    elif request.method == 'PUT':  # collection 수정
        serializer = CollectionSerializer(collection, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    elif request.method == 'DELETE':  # collection 삭제
        collection.delete()

        data = {
            'success': True,
            'message': f'{collection_pk}번 컬렉션 삭제',
        }

        return Response(data, status=status.HTTP_200_OK)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)

# user-collection movie 추가, 삭제
@api_view(['POST', 'DELETE'])
@authentication_classes([])
@permission_classes([])
def create_or_delete_collection_movie(request, collection_pk, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    collection = get_object_or_404(Collection, pk=collection_pk)

    data = {
        'success': True,
        'message': '',
    }
    if request.method == 'POST':  # user-collection movie 추가
        if not collection.movies.filter(pk=movie_pk).exists():  # collection에 movie가 없으면
            collection.movies.add(movie)
            data['message'] = f'{collection_pk}번 컬렉션 {movie.title} 생성'
        else:
            return JsonResponse({ 'success': False })
    elif request.method == 'DELETE':  # user-collection movie 삭제
        if collection.movies.filter(pk=movie_pk).exists():  # collection에 movie가 있으면
            collection.movies.remove(movie)
            data['message'] = f'{collection_pk}번 컬렉션 {movie.title} 삭제'
        else:
            return JsonResponse({ 'success': False })
    
    return JsonResponse(data)


# collection like
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def like_collection(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    ranking = Ranking()
    try:
        # if review.like_users.filter(pk=request.user.pk).exists(): # 좋아요 취소
        if collection.like_users.filter(pk=2).exists():  # test code(request.user 없음)
            # review.like_users.remove(request.user)
            user = get_object_or_404(User, pk=2)
            collection.like_users.remove(user)
            like_status = False

            # review_like 포인트--
            ranking.decrease_collection_like_point(collection)
        else: # 좋아요 누름
            # review.like_users.add(request.user)
            user = get_object_or_404(User, pk=2)
            collection.like_users.add(user)
            like_status = True

            # review_like 포인트++
            ranking.increase_collection_like_point(collection)
        
        data = {
            'success': True,
            'like_status': like_status,
        }
    except:
        return JsonResponse({ 'success': False })
    
    return JsonResponse(data)


# rating =============================================================================================================
# user > movie > rating!
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def set_rating(request, movie_pk):
    input_rating = float(request.POST.get('rating'))
    # user = request.user
    user = get_object_or_404(User, pk=86)  # test code
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    data = { 'success': True, 'rating_status': None, }
    if Movie_User_Rating.objects.filter(user=user, movie=movie).exists():  # 이미 평가를 했다면 수정 or 삭제
        rating = get_object_or_404(Movie_User_Rating, user=user, movie=movie)
        curr_rating = rating.rating
        
        if input_rating == curr_rating:  # 같으면 삭제
            rating.delete()
            data['rating_status'] = 'deleted'
        else:  # 다르면 수정
            rating.rating = input_rating
            rating.save()
            
            data['rating_status'] = 'updated'
    else:  # 평가하지 않았다면 생성
        rating = Movie_User_Rating.objects.create(user=user, movie=movie, rating=input_rating)
        data['rating_status'] = 'created'

    return JsonResponse(data)






# users' movies ======================================================================================================
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_user_top_rated_movies(request, username):
    movie_count = int(request.GET.get('movie_count'))

    user = get_object_or_404(User, username=username)
    ratings = Movie_User_Rating.objects.filter(user=user).order_by('-rating')[:movie_count]
    
    movies = []
    for rating in ratings:
        movie = get_object_or_404(Movie, pk=rating.movie_id)
        movies.append(movie)
    
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def get_user_genre_top_rated_movies(request, username, genre_pk):
    movie_count = int(request.GET.get('movie_count'))

    user = get_object_or_404(User, username=username)
    genre = get_object_or_404(Genre, pk=genre_pk)
    ratings = Movie_User_Genre_Rating.objects.filter(user=user, genre=genre).order_by('-rating')[:movie_count]

    movies = []
    for rating in ratings:
        movie = get_object_or_404(Movie, pk=rating.movie_id)
        movies.append(movie)
    
    serializer = MovieListSerializer(movies, many=True)
    return Response(serializer.data)






# infinity scroll ===========================================================================================
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def infinite_scroll_review(request):
    reviews = get_list_or_404(Review)
    paginator = Paginator(reviews, 9)
    
    page_num = request.GET.get('page_num')

    reviews = paginator.get_page(page_num)
    serializer = ReviewListSerializer(reviews, many=True)
    
    return Response(serializer.data)



















# admin============================================================================================================
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def calc_genre_ranking(request):
    ranking = Ranking()
    ranking.set_genre_ranking()
    # serializers = GenreUserListSerializer(list(users), many=True)
    
    data = {
        'success': True
    }
    return JsonResponse(data)
    # return Response(serializers.data)


# TMP FUNC TO INSERT DATA / admin =================================================================================================
def get_all_movies_from_tmdb(request):
    load_dotenv()
    tmdb_api_key = os.getenv('TMDB_API_KEY')

    for id in range(50):
        URL = f'https://api.themoviedb.org/3/movie/{id}?api_key={tmdb_api_key}&language=ko&region=KR'
        res = requests.get(URL)

        # existed movies only
        if res.status_code == 200:
            data = res.json()
            movie = TmdbMovie(data)
            movie.create_movie()
            print(f'{movie.id} 생성 완료')

    data = {
        'success': True,
    }
    return JsonResponse(data)


def get_seed_rating(request):
    rate_numbers = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    movie_ids = [2,3,5,6,8,9,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,30,31,32,33,35,38]

    seeder = Seed.seeder()
    
    seeder.add_entity(Movie_User_Rating, 400, {
        'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 100)),
        'movie': lambda x: get_object_or_404(Movie, pk=movie_ids[random.randint(0, 28)]),
        'rating': lambda x: rate_numbers[random.randint(0, 9)],
    })
    seeder.execute()

    data = {
        'success': True
    }
    return JsonResponse(data)

def set_seed_genre_rating(request):
    Movie_User_Genre_Rating.objects.all().delete()
    rate_numbers = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
    
    ratings = Movie_User_Rating.objects.all()

    for rating in ratings:
        movie = get_object_or_404(Movie, pk=rating.movie_id)
        user = get_object_or_404(User, pk=rating.user_id)
        
        genres = movie.genres.all()
        rating = rate_numbers[random.randint(0, 9)]
        for genre in genres:
            Movie_User_Genre_Rating.objects.create(
                movie = movie,
                user = user,
                genre = genre,
                rating = rating,
            )
    data = {
        'success': True
    }
    return JsonResponse(data)

def count_ratings(request):
    res = Movie_User_Rating.objects.values('movie').order_by('movie').annotate(total=Sum('rating')).order_by('-total')
    
    for obj in res:
        movie_id = obj.get('movie')
        total = obj.get('total')

        movie = get_object_or_404(Movie, pk=movie_id)
        cnt = Movie_User_Rating.objects.filter(movie=movie_id).count()
        avg = format(total / cnt, '.1f')
        
        # insert data into db
        movie.rating_average = avg
        movie.rating_count = cnt
        movie.save()

    data = {
        'success': True,
    }

    return JsonResponse(data)


def get_seed_review(request):
    movie_ids = [2,3,5,6,8,9,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,30,31,32,33,35,38]
    #user 1~100

    seeder = Seed.seeder()
    
    seeder.add_entity(Review, 200, {
        'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 100)),
        'movie': lambda x: get_object_or_404(Movie, pk=movie_ids[random.randint(0, 28)]),
    })
    seeder.execute()

    data = {
        'success': True
    }
    return JsonResponse(data)

def count_genre_reviews(request):
    reviews = get_list_or_404(Review)
    ranking = Ranking()
    
    # 생성된 review 기반 point 증가
    for review in reviews:
        ranking.increase_review_point(review)

    data = {
        'success': True
    }
    return JsonResponse(data)


def get_seed_comment(request):
    seeder = Seed.seeder()
    
    seeder.add_entity(Comment, 500, {
        'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 100)),
        'review': lambda x: get_object_or_404(Review, pk=random.randint(1, 200)),
    })
    seeder.execute()

    data = {
        'success': True
    }
    return JsonResponse(data)

def count_genre_comments(request):
    comments = get_list_or_404(Comment)

    # 생성된 comment 기반 point 증가
    for comment in comments:
        review = get_object_or_404(Review, pk=comment.review_id)
        ranking = Ranking()
        ranking.increase_comment_point(review)
    
    data = {
        'success': True
    }
    return JsonResponse(data)

# END TMP FUNC TO INSERT DATA==============================================================================================