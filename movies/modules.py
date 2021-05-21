from django.shortcuts import get_object_or_404
from .models import Movie, Genre, BelongsToCollection, ProductionCompany, ProductionCountry, SpokenLanguage


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
                name = self.genres[i].name
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
        
