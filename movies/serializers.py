from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Movie, Genre, Genre_User, Genre_Ranker, Review, Comment, Genre, Collection, Movie_User_Rating

User = get_user_model()

class UserSerailizaer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        exclude = ('movies',)

'''
class BelongsToCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BelongsToCollection
        exclude = ('movies',)

class ProductionCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCompany
        exclude = ('movies',)

class ProductionCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCountry
        exclude = ('movies',)

class SpokenLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        exclude = ('movies',)
'''

class MovieListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'review',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('user', 'review',)


class ReviewSerializer(serializers.ModelSerializer):
    like_users_count = serializers.IntegerField(source='like_users.count', read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('movie', 'user', 'like_users', 'like_users_count')

class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genre
        exclude = ('movies',)

class GenreListSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    class Meta:
        model = Genre
        exclude = ('movies',)

class GenreUserListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = Genre_User
        fields = '__all__'

class GenreRankerSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    class Meta:
        model = Genre_Ranker
        fields = '__all__'
        read_only_fields = ('genre', )

class GenreRankerListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Genre_Ranker
        fields = '__all__'
        read_only_fields = ('genre', )


class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = '__all__'
        read_only_fields = ('user', 'movies', 'like_users',)

class CollectionListSerializer(serializers.ModelSerializer):
    movies = MovieListSerializer(many=True, read_only=True)
    class Meta:
        model = Collection
        fields = '__all__'


class MovieUserRatingSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    class Meta:
        model = Movie_User_Rating
        fields = ('rating', 'movie',)

class MovieUserRatingDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie_User_Rating
        fields = ('rating',)