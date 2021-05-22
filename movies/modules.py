from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model

from .models import Movie, Genre, Genre_User, BelongsToCollection, ProductionCompany, ProductionCountry, SpokenLanguage

User = get_user_model()

class TmdbMovie():
    
    def __init__(self, params):
        def __set_genres__(genre_list):
            class Genre():
                def __init__(self, genre):
                    self.id = genre.get('id')
                    self.name = genre.get('name')
            
            genres = []
            while genre_list:
                tmp_genre = genre_list.pop()
                genre = Genre(tmp_genre)
                genres.append(genre)

            return genres

        def __set_belongs_to_collection__(obj):
            class BelongsToCollection():
                def __init__(self, collect):
                    self.id = collect.get('id')
                    self.name = collect.get('name')
                    self.poster_path = collect.get('poster_path')
                    self.backdrop_path = collect.get('backdrop_path')
            
            if obj is not None:
                return BelongsToCollection(obj)
            else:
                return None
                

        def __set_production_companies__(companies_list):
            class ProductionCompany():
                def __init__(self, company):
                    self.id = company.get('id')
                    self.name = company.get('name')
                    self.logo_path = company.get('logo_path')
                    self.origin_country = company.get('origin_country')
            
            companies = []
            while companies_list:
                tmp_company = companies_list.pop()
                company = ProductionCompany(tmp_company)
                companies.append(company)

            return companies
        
        def __set_production_countries__(countries_list):
            class ProductionCountrie():
                def __init__(self, country):
                    self.iso_3166_1 = country.get('iso_3166_1')
                    self.name = country.get('name')
            
            countries = []
            while countries_list:
                tmp_country = countries_list.pop()
                country = ProductionCountrie(tmp_country)
                countries.append(country)

            return countries

        def __set_spoken_languages__(launguages_list):
            class SpokenLanguage():
                def __init__(self, lang):
                    self.english_name = lang.get('english_name')
                    self.name = lang.get('name')
                    self.iso_639_1 = lang.get('iso_639_1')
            
            languages = []
            while launguages_list:
                tmp_languages = launguages_list.pop()
                language = SpokenLanguage(tmp_languages)
                languages.append(language)

            return languages

        # movie Model
        self.id = params.get('id')
        self.title = params.get('title')
        self.overview = params.get('overview')
        self.poster_path = params.get('poster_path')
        self.release_date = params.get('release_date')
        self.vote_average = params.get('vote_average')
        self.vote_count = params.get('vote_count')
        self.video = params.get('video')
        self.popularity = params.get('popularity')
        self.revenue = params.get('revenue')
        self.runtime = params.get('runtime')
        self.status = params.get('status')
        self.adult = params.get('adult')
        self.budget = params.get('budget')
        self.original_language = params.get('original_language')
        self.original_title = params.get('original_title')
        
        # ManyToManyFields
        self.genres = __set_genres__(params.get('genres'))
        self.belongs_to_collection = __set_belongs_to_collection__(params.get('belongs_to_collection'))
        self.production_companies = __set_production_companies__(params.get('production_companies'))
        self.production_countries = __set_production_countries__(params.get('production_countries'))
        self.spoken_languages = __set_spoken_languages__(params.get('spoken_languages'))


    def create_movie(self):
        # Movie
        movie, created = Movie.objects.get_or_create(
            id = self.id,
            title = self.title,
            overview = self.overview,
            poster_path = self.poster_path,
            release_date = self.release_date,
            vote_average = self.vote_average,
            vote_count = self.vote_count,
            video = self.video,
            popularity = self.popularity,
            revenue = self.revenue,
            runtime = self.runtime,
            status = self.status,
            adult = self.adult,
            budget = self.budget,
            original_language = self.original_language,
            original_title = self.original_title,
            rating_average = 0.0,
            rating_count = 0
            
        )

        # belongs_to_collection
        if self.belongs_to_collection is not None:
            belongs_to_collection, created = BelongsToCollection.objects.get_or_create(
                id = self.belongs_to_collection.id,
                name = self.belongs_to_collection.name,
                poster_path = self.belongs_to_collection.poster_path,
                backdrop_path = self.belongs_to_collection.backdrop_path
            )
            # add ManyToManyField
            movie.belongs_to_collections.add(belongs_to_collection)

        # genre
        for i in range(len(self.genres)):
            genre, created = Genre.objects.get_or_create(
                id = self.genres[i].id,
                name = self.genres[i].name,
                total_review_count = 0
            )
            # add ManyToManyField
            movie.genres.add(genre)
            

        # production_companies
        for i in range(len(self.production_companies)):
            production_company, created = ProductionCompany.objects.get_or_create(
                id = self.production_companies[i].id,
                logo_path = self.production_companies[i].logo_path,
                name = self.production_companies[i].name,
                origin_country = self.production_companies[i].origin_country
            )
            # add ManyToManyField
            movie.production_companies.add(production_company)

        # production_countries
        for i in range(len(self.production_countries)):
            production_country, created = ProductionCountry.objects.get_or_create(
                iso_3166_1 = self.production_countries[i].iso_3166_1,
                name = self.production_countries[i].name
            )
            # add ManyToManyField
            movie.production_countries.add(production_country)

        # spoken_languages
        for i in range(len(self.spoken_languages)):
            spoken_language, created = SpokenLanguage.objects.get_or_create(
                english_name = self.spoken_languages[i].english_name,
                iso_639_1 = self.spoken_languages[i].iso_639_1,
                name = self.spoken_languages[i].english_name
            )
            # add ManyToManyField
            movie.spoken_languages.add(spoken_language)

    def __str__(self):
        return self.title

class Ranking():

    def __init__(self):
        pass
    
    # review
    def increase_review_point(self, review):
        user = get_object_or_404(User, pk=review.user_id)
        movie = get_object_or_404(Movie, pk=review.movie_id)

        genres = movie.genres.all()
        for genre in genres:
            # genre.total_review_count
            genre.total_review_count += 1
            genre.save()
            
            # genre_user
            genre_user = get_object_or_404(Genre_User, genre=genre, user=user)
            genre_user.point += 1
            genre_user.save()

        # user
        user.point += 1
        user.save()
        
    def decrease_review_point(self, review):
        user = get_object_or_404(User, pk=review.user_id)
        movie = get_object_or_404(Movie, pk=review.movie_id)

        genres = movie.genres.all()
        for genre in genres:
            # genre.total_review_count
            genre.total_review_count -= 1
            genre.save()
            
            # genre_user
            genre_user = get_object_or_404(Genre_User, genre=genre, user=user)
            genre_user.point -= 1
            genre_user.save()

        # user
        user.point -= 1
        user.save()


    # review_like
    def increase_review_like_point(self, review):
        user = get_object_or_404(User, pk=review.user_id)
        movie = get_object_or_404(Movie, pk=review.movie_id)

        genres = movie.genres.all()
        for genre in genres:
            # genre_user
            genre_user = get_object_or_404(Genre_User, genre=genre, user=user)
            genre_user.point += 1
            genre_user.save()

        # user
        user.point += 1
        user.save()

    def decrease_review_like_point(self, review):
        user = get_object_or_404(User, pk=review.user_id)
        movie = get_object_or_404(Movie, pk=review.movie_id)

        genres = movie.genres.all()
        for genre in genres:
            # genre_user
            genre_user = get_object_or_404(Genre_User, genre=genre, user=user)
            genre_user.point -= 1
            genre_user.save()

        # user
        user.point -= 1
        user.save()

    # comment 받은 사람
    def increase_comment_point(self, review):
        user = get_object_or_404(User, pk=review.user_id)
        movie = get_object_or_404(Movie, pk=review.movie_id)

        genres = movie.genres.all()
        for genre in genres:
            # genre_user
            genre_user = get_object_or_404(Genre_User, genre=genre, user=user)
            genre_user.point += 1
            genre_user.save()

        # user
        user.point += 1
        user.save()

    def decrease_comment_point(self, review):
        user = get_object_or_404(User, pk=review.user_id)
        movie = get_object_or_404(Movie, pk=review.movie_id)

        genres = movie.genres.all()
        for genre in genres:
            # genre_user
            genre_user = get_object_or_404(Genre_User, genre=genre, user=user)
            genre_user.point -= 1
            genre_user.save()

        # user
        user.point -= 1
        user.save()


    # collection_like
    def increase_collection_like_point(self, collection):
        user = get_object_or_404(User, pk=collection.user_id)
        user.point += 1
        user.save()

    def decrease_collection_like_point(self, collection):
        user = get_object_or_404(User, pk=collection.user_id)
        user.point -= 1
        user.save()



    # genre_user set_ranking
    def set_genre_ranking(self):
        genre_ids = [12, 14, 16, 18, 27, 28, 35, 36, 37, 53, 80, 99, 878, 9648, 10402, 10749, 10751, 10752]
        for genre_id in genre_ids:
            genre_users = Genre_User.objects.filter(genre_id=genre_id).order_by('-point')

            tmp_i = 0
            tmp_p = 0
            for i in range(len(genre_users)):
                genre_user = genre_users[i]
                p = genre_user.point
                if i == 0:
                    genre_user.ranking = i+1
                    genre_user.save()
                    tmp_i = i+1
                    tmp_p = p
                else:
                    if p == tmp_p:
                        genre_user.ranking = tmp_i
                        genre_user.save()
                    else:
                        genre_user.ranking = i+1
                        genre_user.save()
                        tmp_i = i+1
                        tmp_p = p
        return



import os
import random
import requests
from dotenv import load_dotenv, dotenv_values

from django_seed import Seed
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum

from .models import Comment, Movie_User_Rating, Movie_User_Genre_Rating, Review
class InsertData():
    def my_exec(self):
        self.get_all_movies_from_tmdb()
        self.get_seed_users()
        self.get_seed_review()
        self.get_seed_comment()
        self.get_seed_rating()
        self.set_seed_genre_rating()
        self.count_genre_reviews()
        self.count_genre_comments()
        self.count_ratings()

    def get_all_movies_from_tmdb(self):
        Movie.objects.all().delete()  # movie 정보 삭제
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


    def get_seed_users(self):
        print('유저 생성 시작')
        seeder = Seed.seeder()
    
        seeder.add_entity(User, 100, {
            'point': lambda x: random.randint(1, 100),
            'ranking': 0,
            'tier': 0,
        })
        seeder.execute()

        # tmp user genre
        for i in range(1, 101):
            user = get_object_or_404(User, pk=i)
            self.set_genre_user(user)
            
        print('user 생성 완료')

    def set_genre_user(self, user):
        genre_ids = [12, 14, 16, 18, 27, 28, 35, 36, 37, 53, 80, 99, 878, 9648, 10402, 10749, 10751, 10752]
        for genre_id in genre_ids:
            genre = get_object_or_404(Genre, pk=genre_id)
            
            genre_user, created = Genre_User.objects.get_or_create(
                user = user,
                genre = genre,
            )


    def get_seed_rating(self):
        rate_numbers = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        movie_ids = [2,3,5,6,8,9,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,30,31,32,33,35,38]

        seeder = Seed.seeder()
        
        seeder.add_entity(Movie_User_Rating, 400, {
            'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 100)),
            'movie': lambda x: get_object_or_404(Movie, pk=movie_ids[random.randint(0, 28)]),
            'rating': lambda x: rate_numbers[random.randint(0, 9)],
        })
        seeder.execute()

        print('평점 생성 완료')

    def set_seed_genre_rating(self):
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
        
        print('평가 결과 바탕 장르별 영화 평점 계산 완료')

    def count_ratings(self):
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

        print('평점 계산 완료')


    def get_seed_review(self):
        movie_ids = [2,3,5,6,8,9,11,12,13,14,15,16,17,18,19,20,21,22,24,25,26,27,28,30,31,32,33,35,38]

        seeder = Seed.seeder()
        
        seeder.add_entity(Review, 200, {
            'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 100)),
            'movie': lambda x: get_object_or_404(Movie, pk=movie_ids[random.randint(0, 28)]),
        })
        seeder.execute()

        print('review 정보 생성 완료')

    def count_genre_reviews(self):
        reviews = get_list_or_404(Review)
        ranking = Ranking()
        
        # 생성된 review 기반 point 증가
        for review in reviews:
            ranking.increase_review_point(review)

        print('review 기반 유저별 장르 포인트 계산 완료')


    def get_seed_comment(self):
        seeder = Seed.seeder()
        
        seeder.add_entity(Comment, 500, {
            'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 100)),
            'review': lambda x: get_object_or_404(Review, pk=random.randint(1, 200)),
        })
        seeder.execute()

        print('comment 생성 완료')

    def count_genre_comments(self):
        comments = get_list_or_404(Comment)

        # 생성된 comment 기반 point 증가
        for comment in comments:
            review = get_object_or_404(Review, pk=comment.review_id)
            ranking = Ranking()
            ranking.increase_comment_point(review)
        
        print('comment 기반 유저별 장르 포인트 계산 완료')