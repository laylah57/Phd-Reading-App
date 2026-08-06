# Serializers define the API representation.
from django.contrib.auth.models import User, Group
from django.db.models import Model
from rest_framework import serializers, request
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer

from phd_reading_app.models import ReadingItem, Author, Tag, Status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field].required = False

    def validate(self, attrs):
        email = attrs['email']
        user = User.objects.filter(email=email).first()

        if not user:
            raise AuthenticationFailed(
                self.error_messages["No active account"],
                'no active account',
            )

        attrs['username'] = user.username
        return super().validate(attrs)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']

class ReadingItemSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True)
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = ReadingItem
        fields = [
            'id',
            'title',
            'subtitle',
            'year_published',
            'created_at',
            'status',
            'tags',
            'authors',
        ]

    def create(self, validated_data):
        authors_data = validated_data.pop('authors', [])
        tags_data = validated_data.pop('tags', [])

        reading_item = ReadingItem.objects.create(**validated_data)

        for author_data in authors_data:
            author, created = Author.objects.get_or_create(**author_data)
            reading_item.authors.add(author)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            reading_item.tags.add(tag)

        return reading_item
