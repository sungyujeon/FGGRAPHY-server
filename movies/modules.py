from django.shortcuts import get_list_or_404, get_object_or_404
from django.contrib.auth import get_user_model

from .models import Movie, Genre, Genre_User, Genre_Ranker, Movie_User_Genre_Rating

User = get_user_model()
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
        total_users = User.objects.all().count()
        tier_1 = int(total_users * 0.15)
        tier_2 = int(total_users * 0.3)
        tier_3 = int(total_users * 0.45)
        tier_4 = int(total_users * 0.6)
        def calc_tier(r, tier1, tier2, tier3, tier4):
            if 1 < r <= tier1:
                return 1
            elif r <= tier2:
                return 2
            elif r <= tier3:
                return 3
            elif r <= tier4:
                return 4
            else:
                return 5

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
                    genre_user.tier = i
                    genre_user.save()
                    tmp_i = i+1
                    tmp_p = p
                else:
                    if p == tmp_p:
                        genre_user.ranking = tmp_i
                        t = calc_tier(tmp_i, tier_1, tier_2, tier_3, tier_4)
                        genre_user.tier = t
                        genre_user.save()
                    else:
                        genre_user.ranking = i+1
                        t = calc_tier(i+1, tier_1, tier_2, tier_3, tier_4)
                        genre_user.tier = t
                        genre_user.save()
                        tmp_i = i+1
                        tmp_p = p

            # genre_id의 1등 유저
            genre = get_object_or_404(Genre, pk=genre_id)
            top_genre_user = get_object_or_404(User, pk=genre_users[0].user_id)
            genre_user_rating = Movie_User_Genre_Rating.objects.filter(genre=genre, user=top_genre_user).order_by('-rating')[0]
            
            genre_ranker = get_object_or_404(Genre_Ranker, genre=genre)
            if not genre_ranker.movie or genre_ranker != top_genre_user:
                movie = get_object_or_404(Movie, pk=genre_user_rating.movie_id)
                genre_ranker.user = top_genre_user
                genre_ranker.movie = movie
                genre_ranker.save()
            else:
                print(f'{genre.name} 장르 순위 변동사항 없음')
        
        print('장르별 랭킹 계산 완료')

    # init genre ranker model
    def init_genre_ranker_model(self):
        genre_ids = [12, 14, 16, 18, 27, 28, 35, 36, 37, 53, 80, 99, 878, 9648, 10402, 10749, 10751, 10752]

        for genre_id in genre_ids:
            genre = get_object_or_404(Genre, pk=genre_id)
            
            genre_ranker, created = Genre_Ranker.objects.get_or_create(
                genre = genre,
            )
        print('init genre ranker model 완료')
            
class TMDBMovie():

    def __init__(self, params, rt, mg):

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
        
        # movie Model
        self.id = params.get('id')
        self.title = params.get('title')
        self.overview = params.get('overview')
        self.backdrop_path = params.get('backdrop_path')
        self.poster_path = params.get('poster_path')
        self.release_date = params.get('release_date')
        self.vote_average = params.get('vote_average')
        self.vote_count = params.get('vote_count')
        self.video = params.get('video')
        self.popularity = params.get('popularity')
        self.runtime = rt
        self.adult = params.get('adult')
        self.original_language = params.get('original_language')
        self.original_title = params.get('original_title')
        
        # ManyToManyFields
        self.genres = __set_genres__(mg)


    def create_movie(self):
        # Movie
        movie, created = Movie.objects.get_or_create(
            id = self.id,
            title = self.title,
            overview = self.overview,
            poster_path = self.poster_path,
            backdrop_path = self.backdrop_path,
            release_date = self.release_date,
            vote_average = self.vote_average,
            vote_count = self.vote_count,
            video = self.video,
            popularity = self.popularity,
            runtime = self.runtime,
            adult = self.adult,
            original_language = self.original_language,
            original_title = self.original_title,
            rating_average = 0.0,
            rating_count = 0
        )

        # genre
        for i in range(len(self.genres)):
            genre, created = Genre.objects.get_or_create(
                id = self.genres[i].id,
                name = self.genres[i].name,
                total_review_count = 0
            )
            # add ManyToManyField
            movie.genres.add(genre)

    def __str__(self):
        return self.title



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
        return False
        # self.get_all_movies_by_popularity()
        # self.get_seed_users()
        # self.get_seed_review()
        # self.get_seed_comment()
        # self.get_seed_rating()
        # self.set_seed_genre_rating()
        # self.count_genre_reviews()
        # self.count_genre_comments()
        # self.count_ratings()
        # self.get_all_movies_from_tmdb()
        # self.remove_user()
    
    def remove_user(self):
        user_len = User.objects.all().count()
        for i in range(101, user_len+1):
            user = get_object_or_404(User, pk=i)
            user.delete()
        print('에러 유저 삭제 완료')

    # def get_all_movies_from_tmdb(self):
    #     Movie.objects.all().delete()  # movie 정보 삭제
    #     load_dotenv()
    #     tmdb_api_key = os.getenv('TMDB_API_KEY')

    #     for id in range(50):
    #         URL = f'https://api.themoviedb.org/3/movie/{id}?api_key={tmdb_api_key}&language=ko&region=KR'
    #         res = requests.get(URL)

    #         # existed movies only
    #         if res.status_code == 200:
    #             data = res.json()
    #             movie = TmdbMovie(data)
    #             movie.create_movie()
    #             print(f'{movie.id} 생성 완료')
    def get_all_movies_by_popularity(self):
        load_dotenv()
        tmdb_api_key = os.getenv('TMDB_API_KEY')
        for i in range(1, 300):
            URL = f'https://api.themoviedb.org/3/discover/movie?page={i}&sort_by=popularity.desc&api_key={tmdb_api_key}&language=ko&region=KR'
            res = requests.get(URL)
            if res.status_code == 200:
                movies = res.json().get('results')
                
                for res_movie in movies:
                    movie_id = res_movie.get('id')
                    idURL = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}&language=ko&region=KR'
                    idRes = requests.get(idURL)

                    if idRes.status_code == 200:
                        idData = idRes.json()
                        movie_runtime = idData.get('runtime')
                        movie_genres = idData.get('genres')
                    else:
                        movie_runtime = None
                        idGenres = None
                    
                    movie = TMDBMovie(res_movie, movie_runtime, movie_genres)
                    movie.create_movie()
                    print(f'{movie.title} 생성 완료')

    def get_seed_users(self):
        print('유저 생성 시작')
        seeder = Seed.seeder()
    
        seeder.add_entity(User, 1, {
            'point': 0,
            'ranking': None,
            'tier': 5,
        })
        seeder.execute()

        # tmp user genre
        for i in range(2, 50):
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


    def __get_movie_ids__(self):
        tmp_movie_ids = []
        tmp_movies = Movie.objects.all()
        for tmp_movie in tmp_movies:
            tmp_movie_ids.append(tmp_movie.id)
        return tmp_movie_ids

    def get_seed_rating(self):
        # Movie_User_Rating.objects.create(rating=3.0, movie=get_object_or_404(Movie, pk=99), user=get_object_or_404(User, pk=3))
            
        movie_ids = self.__get_movie_ids__()
        rate_numbers = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
        

        seeder = Seed.seeder()
        
        seeder.add_entity(Movie_User_Rating, 1000, {
            'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 20)),
            'movie': lambda x: get_object_or_404(Movie, pk=movie_ids[random.randint(100, 4444)]),
            'rating': lambda x: rate_numbers[random.randint(0, 9)],
        })
        seeder.execute()

        print('평점 생성 완료')

    def set_seed_genre_rating(self):
        ratings = Movie_User_Rating.objects.all()

        for rating in ratings:
            movie = get_object_or_404(Movie, pk=rating.movie_id)
            user = get_object_or_404(User, pk=rating.user_id)
            rating_num = rating.rating
            
            genres = movie.genres.all()
            for genre in genres:
                Movie_User_Genre_Rating.objects.create(
                    movie = movie,
                    user = user,
                    genre = genre,
                    rating = rating_num,
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
        # Review.objects.get_or_create(content='review', movie=get_object_or_404(Movie, pk=99), user=get_object_or_404(User, pk=3))
        movie_ids = self.__get_movie_ids__()

        seeder = Seed.seeder()
        
        seeder.add_entity(Review, 500, {
            'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(1, 20)),
            'movie': lambda x: get_object_or_404(Movie, pk=movie_ids[random.randint(100, 4000)]),
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
            'user': lambda x: get_object_or_404(get_user_model(), pk=random.randint(2, 20)),
            'review': lambda x: get_object_or_404(Review, pk=random.randint(1, 300)),
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




'''
class TmdbMovieById():
    
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
'''