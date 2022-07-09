from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Author


# Create your tests here.
class BaseSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create_user(
            username="sam", password="1234"
        )

        cls.user_2 = get_user_model().objects.create_user(
            username="davidd", password="abcdef"
        )

        cls.author = Author.objects.create(
            user=cls.user_1,
            first_name="samuel",
            last_name="king",
            image="my_profile_pic.jpg",
            email="kingsam@example.com",
            bio="i hate writing tests",
        )


class AuthorModelTest(BaseSetUp):
    def test_string_method(self):
        self.assertEqual(self.author.__str__(), "samuel king")

    def test_save_method_adds_a_slug(self):
        self.assertEqual(self.author.slug, "samuel-king")

    def test_get_absolute_url(self):
        self.assertEqual(self.author.get_absolute_url(), "/authors/samuel-king/")


class AuthorsViewTest(BaseSetUp):
    def test_that_the_view_url_exists(self):
        response = self.client.get("/authors/")
        self.assertEqual(response.status_code, 200)

    def test_that_url_exists_by_name(self):
        response = self.client.get(reverse("authors:authors"))
        self.assertEqual(response.status_code, 200)

    def test_that_view_renders_correct_template(self):
        response = self.client.get("/authors/")
        self.assertTemplateUsed(response, "authors/authors_page.html")
        self.assertContains(response, "Authors")

    def test_that_view_returns_correct_queryset(self):
        qs = Author.objects.all()
        self.assertQuerysetEqual(qs, values=[self.author])


class AuthorDetailViewTest(BaseSetUp):
    def test_author_detail_view_url_exists(self):
        response = self.client.get("/authors/samuel-king/")
        self.assertEqual(response.status_code, 200)

    def test_that_view_url_exists_by_name(self):
        response = self.client.get(
            reverse("authors:author_detail", args=["samuel-king"])
        )
        self.assertEqual(response.status_code, 200)

    def test_that_view_renders_correct_template(self):
        response = self.client.get("/authors/samuel-king/")
        self.assertTemplateUsed(response, "authors/author_detail_page.html")
        self.assertContains(response, "About Samuel King")


class BecomeAuthorViewTest(BaseSetUp):
    def test_that_view_url_exists(self):
        self.client.login(username="sam", password="1234")
        response = self.client.get("/authors/join/become-an-author/")
        self.assertEqual(response.status_code, 200)

    def test_that_view_url_exists_by_name(self):
        self.client.login(username="sam", password="1234")
        response = self.client.get(reverse("authors:become_author"))
        self.assertEqual(response.status_code, 200)

    def test_that_view_requires_login(self):
        response = self.client.get("/authors/join/become-an-author/")
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, "/users/login/?next=/authors/join/become-an-author/"
        )

    def test_that_view_renders_correct_template(self):
        self.client.login(username="sam", password="1234")
        response = self.client.get("/authors/join/become-an-author/")
        self.assertTemplateUsed(response, "authors/become_author.html")
        self.assertContains(response, "Become an author")

    def test_that_user_can_become_author(self):
        self.client.login(username="davidd", password="abcdef")
        response = self.client.post(
            "/authors/join/become-an-author/",
            {
                "first_name": "David",
                "last_name": "Joshua",
                "email": "davej@blog.co",
                "bio": "i like running tests",
            },
        )
        self.assertEqual(response.status_code, 200)  # should be 302


class EditAuthorProfileViewTest(BaseSetUp):
    def test_that_the_view_url_exists(self):
        self.client.login(username="sam", password="1234")
        response = self.client.get("/authors/samuel-king/edit-profile/")
        self.assertEqual(response.status_code, 200)

    def test_that_view_renders_correct_template(self):
        self.client.login(username="sam", password="1234")
        response = self.client.get("/authors/samuel-king/edit-profile/")
        self.assertTemplateUsed(response, "authors/author_edit_profile.html")

    def test_that_view_requires_login(self):
        response = self.client.get("/authors/samuel-king/edit-profile/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/users/login/?next=/authors/samuel-king/edit-profile/"
        )

    def test_edit_author_profile(self):
        self.client.login(username="sam", password="1234")
        response = self.client.post(
            "/authors/samuel-king/edit-profile/",
            {
                "first_name": "Martin",
                "last_name": "James",
                "email": "kingsam@example.com",
                "bio": "i love running tests",
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_that_an_author_cannot_edit_another_author_profile(self):
        self.client.login(username="davidd", password="abcdef")
        get_response = self.client.post("/authors/samuel-king/edit-profile/")
        post_response = self.client.post(
            "/authors/samuel-king/edit-profile/", {"bio": "i love running tests"}
        )
        self.assertEqual(get_response.status_code, post_response.status_code, 403)
