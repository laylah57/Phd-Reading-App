from django.contrib.auth.models import User, Group
from django.db.models import Model
from django.shortcuts import render
from rest_framework import viewsets, permissions, response, views, request
from rest_framework_simplejwt.views import TokenObtainPairView

from phd_reading_app.models import ReadingItem, Tag, Author
from phd_reading_app.serializers import UserSerializer, GroupSerializer, EmailTokenObtainPairSerializer, \
    ReadingItemSerializer, TagSerializer, AuthorSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmailTokenObtainPairViewSet(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer

class CurrentUserViewSet(views.APIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]  # IsAuthenticated = only authenticated users can access the view (in our
    # case, a valid JWT token is included in the request. It is used before get() runs. Used by the APIView class
    # under the hood so we don't have to do conditional logic.
    def get(self, request):
        serializer = UserSerializer(request.user)
        return response.Response(serializer.data)

class ReadingItemViewSet(viewsets.ModelViewSet):
    queryset = ReadingItem.objects.all().order_by('created_at')
    serializer_class = ReadingItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        print(request)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('last_name')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]
