from django.db import models
from django.conf import settings



class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.TextField()
    overview = models.TextField(null=True, blank=True)
    poster_path = models.TextField(null=True, blank=True)
    backdrop_path = models.TextField(null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.IntegerField(null=True, blank=True)
    vote_count = models.IntegerField(null=True, blank=True)
    video = models.TextField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    runtime = models.IntegerField(null=True, blank=True)
    adult = models.BooleanField(null=True, blank=True)
    original_language = models.CharField(max_length=20, null=True, blank=True)
    original_title = models.TextField(null=True, blank=True)
    rating_average = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)


class Genre(models.Model):
    movies = models.ManyToManyField(Movie, related_name='genres')
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=20)
    total_review_count = models.IntegerField(default=0)

class Movie_User_Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.FloatField()

class Movie_User_Genre_Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    rating = models.FloatField()

class Genre_User(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    point = models.IntegerField(default=0)
    ranking = models.IntegerField(null=True, default=10000000)
    tier = models.IntegerField(null=True, default=5)


class Genre_Ranker(models.Model):
    genre = models.OneToOneField(Genre, unique=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, default=None)

class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Collection
class Collection(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie, related_name='collections')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_collections')
    title = models.CharField(max_length=50)
    


'''
class BelongsToCollection(models.Model):
    movies = models.ManyToManyField(Movie, related_name='belongs_to_collections')
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
'''