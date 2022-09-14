from django.test import TestCase
from django.contrib.auth import get_user_model


# Create your tests here.
class UserTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            username="testuser3", password="django-tests12"
        )
        return super().setUp()

    def test_register_page_exists(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_user_can_register(self):
        response = self.client.post(
            "/register/",
            {
                "username": "testuserx",
                "password": "django-test12",
                "confirm_password": "django-test12",
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_login_page_exists(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_user_can_login(self):
        response = self.client.post(
            "/login/", {"username": "testuser3", "password": "django-test12"}
        )
        self.assertEqual(response.status_code, 200)

    def test_logout_page_exists(self):
        response = self.client.post("/logout/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "logged out successfully")
        self.assertTemplateUsed(response, "registration/logged_out.html")
