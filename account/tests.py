from django.test import TestCase
from .models import *
from django.contrib.auth import authenticate, login


class AccountModelTest(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(email="john@mail.com", username="JohnDoe",
            password="JohnDoe123", name="John", surname="Doe", age=17, gender=Account.MALE, location_node_id=12365849)

        self.superuser = Account.objects.create_superuser(email="Admin@mail.com", username="Admin",
            password="Admin123", name="Admin", surname="Admin", age=22, gender=Account.MALE, location_node_id=564782139)  


    def test_create_user(self):  
        self.assertEqual(self.user.email, "john@mail.com")
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_superuser, False)


    def test_create_superuser(self):
        self.assertEqual(self.superuser.email, "Admin@mail.com")
        self.assertEqual(self.superuser.is_staff, True)
        self.assertEqual(self.superuser.is_superuser, True)


    def test_authenticate(self):
        user = authenticate(email="john@mail.com", password="JohnDoe123")
        self.assertNotEqual(user, None)
