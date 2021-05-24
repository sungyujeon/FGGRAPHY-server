from django.contrib.auth import get_user_model
User = get_user_model()

from .modules import TmdbMovie, Ranking
from .models import Movie, Movie_User_Rating, Movie_User_Genre_Rating, Review, Comment, Genre, Genre_User, Collection, Genre_Ranker
from .serializers import MovieListSerializer, MovieSerializer, ReviewSerializer, CommentListSerializer, CommentSerializer, GenreListSerializer, GenreSerializer, GenreUserListSerializer, GenreRankerListSerializer, CollectionListSerializer, CollectionSerializer, MovieUserRatingSerializer

from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_movies(request):
    movies = get_list_or_404(Movie)
    serializer = MovieListSerializer(movies, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSerializer(movie)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_top_rated_movies(request):
    movie_count = int(request.GET.get('movie_count'))
    movies = Movie.objects.all().order_by('-rating_average')[:movie_count]
    serializer = MovieListSerializer(list(movies), many=True)

    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_top_ranked_users_movies(request):
    try:
        ranker_num = int(request.GET.get('ranker_num'))
    except:
        ranker_num = 5
    try:
        movie_num = int(request.GET.get('movie_num'))
    except:
        movie_num = 10

    data = []
    users = User.objects.all().order_by('ranking')[:ranker_num]
    for i in range(len(users)):
        ratings = Movie_User_Rating.objects.filter(user=users[i]).order_by('-rating')[:movie_num]
        serializer = MovieUserRatingSerializer(ratings, many=True)
        tmp = {
            'username': users[i].username,
            'movies': serializer.data,
        }
        data.append(tmp)
    
    return JsonResponse(data, safe=False)



# review ======================================================================
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_or_create_reviews(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == 'GET':  # 전체 review 조회 
        reviews = movie.review_set.all()
        serializers = ReviewSerializer(list(reviews), many=True)
        print(serializers)
        
        return Response(serializers.data)
    elif request.method == 'POST':  # review 생성
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            review = serializer.save(user=request.user, movie=movie)

            # review 생성 시 point 증가
            ranking = Ranking()
            ranking.increase_review_point(review)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)

@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_or_update_or_delete_review(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':  # 단일 review 조회 
        serializers = ReviewSerializer(review)

        return Response(serializers.data)
    elif request.method == 'PUT':  # review 수정
        serializer = ReviewSerializer(review, data=request.data)

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

# latest review list
@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_latest_reviews(request, username):
    try:
        review_num = int(request.GET.get('review_num'))
    except:
        review_num = 10

    user = get_object_or_404(User, username=username)
    reviews = Review.objects.filter(user=user).order_by('updated_at')[:review_num]
    
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)


# review like
@api_view(['POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like_review(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    ranking = Ranking()
    like_status = False
    try:
        if review.like_users.filter(pk=request.user.pk).exists(): # 좋아요 취소
            review.like_users.remove(request.user)
            like_status = False

            # review_like 포인트--
            ranking.decrease_review_like_point(review)
        else: # 좋아요 누름
            review.like_users.add(request.user)
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_or_create_comments(request, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.method == 'GET':  # 전체 comments 조회 
        comments = review.comment_set.all()
        serializers = CommentListSerializer(list(comments), many=True)

        return Response(serializers.data)
    elif request.method == 'POST':  # comment 생성
        serializer = CommentListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, review=review)
            
            # comment 받은 사람 point++
            ranking = Ranking()
            ranking.increase_comment_point(review)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_genres(request):  # 전체 장르 정보
    genres = get_list_or_404(Genre)
    serializer = GenreListSerializer(genres, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_genre_datas(request, genre_pk):  # 개별 장르 정보
    genre = get_object_or_404(Genre, pk=genre_pk)
    serializer = GenreSerializer(genre)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_genre_all_movies(request, genre_pk):  # 개별 장르의 모든 영화 정보
    genre = get_object_or_404(Genre, pk=genre_pk)
    movies = genre.movies.all()
    serializer = MovieListSerializer(list(movies), many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_top_reviewed_genres(request):  # 장르별 리뷰순
    genres = Genre.objects.all().order_by('-total_review_count')
    serializer = GenreListSerializer(genres, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
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

@api_view(['GET'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_genre_ranking_page_data(request):
    genre_rankers = get_list_or_404(Genre_Ranker)
    genre_rankers.sort(key = lambda x: x.genre.total_review_count, reverse=True)
    
    serializer = GenreRankerListSerializer(genre_rankers, many=True)

    return Response(serializer.data)
    


# collections ====================================================================================
@api_view(['GET', 'POST'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def get_or_create_collections(request):
    if request.method == 'GET':  # 전체 collections 조회 
        collections = get_list_or_404(Collection)
        serializers = ReviewSerializer(collections, many=True)

        return Response(serializers.data)
    elif request.method == 'POST':  # collection 생성
        serializer = CollectionSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(User, pk=request.user.id)
            collection = serializer.save(user=user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    data = {
        'success': False,
    }
    
    return JsonResponse(data)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def like_collection(request, collection_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    ranking = Ranking()
    try:
        if collection.like_users.filter(pk=request.user.pk).exists(): # 좋아요 취소
            collection.like_users.remove(request.user)
            like_status = False

            # review_like 포인트--
            ranking.decrease_collection_like_point(collection)
        else: # 좋아요 누름
            collection.like_users.add(request.user)
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def set_rating(request, movie_pk):
    input_rating = float(request.POST.get('rating'))
    user = request.user
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JSONWebTokenAuthentication])
@permission_classes([IsAuthenticated])
def infinite_scroll_review(request, pk):
    # review가 달린 영화가 어떤 영화인지 알기위해
    movie = get_object_or_404(Movie, pk=pk)
    # 해당 영화에 관련된 리뷰만 가져오기
    reviews = Review.objects.filter(movie=movie)
    paginator = Paginator(reviews, 9)
    
    page_num = request.GET.get('page_num')

    reviews = paginator.get_page(page_num)
    serializer = ReviewSerializer(reviews, many=True)
    
    return Response(serializer.data)







# admin============================================================================================================
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def calc_genre_ranking(request):
    ranking = Ranking()
    ranking.set_genre_ranking()
    
    data = {
        'success': True
    }
    return JsonResponse(data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def init_genre_ranker(request):
    ranking = Ranking()
    ranking.init_genre_ranker_model()
    
    data = {
        'success': True
    }
    return JsonResponse(data)


# insert data
from .modules import InsertData
def insert_data(request):
    insert = InsertData()
    insert.my_exec()
    
    data = {
        'success': True
    }
    return JsonResponse(data)