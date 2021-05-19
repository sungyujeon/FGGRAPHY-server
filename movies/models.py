from django.db import models


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    overview = models.TextField(null=True, blank=True)
    poster_path = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.IntegerField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    video = models.TextField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    revenue = models.IntegerField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    adult = models.BooleanField(null=True, blank=True)
    budget = models.IntegerField(null=True, blank=True)
    original_language = models.CharField(max_length=20, null=True, blank=True)
    original_title = models.TextField(null=True, blank=True)

class Genre(models.Model):
    movies = models.ManyToManyField(Movie, related_name='genres')
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=20)

class BelongsToCollection(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.TextField(null=True, blank=True)
    poster_path = models.TextField(null=True, blank=True)
    backdrop_path = models.TextField(null=True, blank=True)

class ProductionCompany(models.Model):
    movies = models.ManyToManyField(Movie, related_name='production_companies')
    id = models.IntegerField(primary_key=True, unique=True)
    logo_path = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    origin_country = models.TextField(null=True, blank=True)

class ProductionCountry(models.Model):
    movies = models.ManyToManyField(Movie, related_name='production_countries')
    iso_3166_1 = models.CharField(max_length=20, unique=True)
    name = models.TextField()


class SpokenLanguage(models.Model):
    movies = models.ManyToManyField(Movie, related_name='spoken_languages')
    english_name = models.CharField(max_length=50, unique=True)
    iso_639_1 = models.CharField(max_length=20)
    name = models.CharField(max_length=20)