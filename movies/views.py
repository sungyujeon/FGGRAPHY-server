# tmp libraries
from pprint import pprint
# end tmp libraries

from django.contrib.auth import get_user_model
User = get_user_model()

from .modules import TmdbMovie
from .models import Movie, Movie_User_Rating, Review, Comment, Genre
from .serializers import MovieListSerializer, MovieSerializer, ReviewListSerializer, ReviewSerializer, CommentListSerializer, CommentSerializer, GenreListSerializer, GenreSerializer

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
def get_top_rated_movies(request, count):
    movies = Movie.objects.all().order_by('-rating_average')[:count]
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
            serializer.save(user=user, movie=movie)

            # 해당 영화의 장르 review_count 증가
            genres = movie.genres.all()
            for genre in genres:
                genre.total_review_count += 1
                genre.save()

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

        # 해당 영화의 장르 review_count 감소
        movie = get_object_or_404(Movie, pk=review.movie_id)
        genres = movie.genres.all()
        for genre in genres:
            genre.total_review_count -= 1
            genre.save()

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

    try:
        # if review.like_users.filter(pk=request.user.pk).exists(): # 좋아요 취소
        if review.like_users.filter(pk=5).exists():  # test code(request.user 없음)
            # review.like_users.remove(request.user)
            user = get_object_or_404(User, pk=5)
            review.like_users.remove(user)
        else: # 좋아요 누름
            # review.like_users.add(request.user)
            user = get_object_or_404(User, pk=5)
            review.like_users.add(user)
        
        data = {
            'success': True,
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
            user = get_object_or_404(User, pk=3)
            serializer.save(user=user, review=review)
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

    for review in reviews:
        movie = get_object_or_404(Movie, pk=review.movie_id)
        
        genres = movie.genres.all()
        for genre in genres:
            genre.total_review_count += 1
            genre.save()
    
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

# END TMP FUNC TO INSERT DATA==============================================================================================