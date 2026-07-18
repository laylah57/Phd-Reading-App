from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class CurrentUserAPITest(APITestCase):
    def test_cannot_access_user_endpoint_without_authentication(self):
        response = self.client.get("/me/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_access_user_endpoint_when_authenticated(self):
        #group = Group.objects.create(name="ADMINISTRATEUR")
        test_user = User.objects.create_user(
            username="John", email="john@doe.com", password="password123"
        )
        #test_user.groups.add(group)
        self.client.force_authenticate(user=test_user)
        response = self.client.get("/me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "John")
        #self.assertEqual(response.data["groups"], ["ADMINISTRATEUR"])
