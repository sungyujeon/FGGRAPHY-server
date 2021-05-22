from django.shortcuts import get_object_or_404
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

    