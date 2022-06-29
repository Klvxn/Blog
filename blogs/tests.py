from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from authors.models import Author

from .models import BlogPost, Comment


# Create your tests here.
class BaseSetUp(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

        cls.user_2 = get_user_model().objects.create_user(
            username="mantis", password="9wen3231"
        )

        cls.author = Author.objects.create(
            user=cls.user_1,
            first_name="Samson",
            last_name="Gregor",
            email="gresam@blogs.xo",
            bio="I am a django developer",
        )

        cls.blog = BlogPost.objects.create(
            title="first test", text="this is my first test", author=cls.author
        )

        cls.comment = Comment.objects.create(
            post=cls.blog, username="testuser2", text="test the comment section"
        )


class BlogPostModelTest(BaseSetUp):
    def test_str_method(self):
        post = self.blog
        self.assertEqual(post.__str__(), "first test by Samson Gregor")

    def test_get_absolute_url(self):
        self.assertEqual(self.blog.get_absolute_url(), "/posts/first-test/1/")

    def test_date_of_blogpost(self):
        current_date = timezone.now().date()
        self.assertEqual(self.blog.date_added.date(), current_date)

    def test_slug_of_blogpost(self):
        self.assertEqual(self.blog.slug, "first-test")


class CommentModelTest(BaseSetUp):
    def test_str_method(self):
        comment = self.comment
        self.assertEqual(comment.__str__(), "test the comment section by testuser2")

    def test_date_of_comment(self):
        date = timezone.now().date()
        self.assertEqual(self.comment.date_created.date(), date)


class IndexViewTest(TestCase):
    def test_that_view_url_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Blog")

    def test_that_view_url_exists_by_name(self):
        response = self.client.get(reverse("blogs:index"))
        self.assertEqual(response.status_code, 200)

    def test_that_view_renders_correct_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "blogs/index.html")

    def test_search_bar_is_in_indexpage(self):
        response = self.client.get("/")
        self.assertContains(response, "Search")


class PostDetailViewTest(BaseSetUp):
    def test_view_url_exists(self):
        response = self.client.get("/posts/first-test/1/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_by_name(self):
        response = self.client.get(
            reverse("blogs:post_detail", args=[self.blog.slug, self.blog.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template(self):
        response = self.client.get("/posts/first-test/1/")
        self.assertTemplateUsed(response, "blogs/post_detail.html")
        self.assertContains(response, "first test")

    def test_post_source_is_not_more_than_50_characters(self):
        post = self.blog
        post.source = "www.example.co/this-is-not-a-real-link/trying-to-test-my-source/"
        post.save()
        self.assertEqual(len(post.source), 50)

    def test_comment_section_exists_in_a_post(self):
        response = self.client.get("/posts/first-test/1/")
        self.assertContains(response, "Comments", status_code=200)

    def test_users_can_comment_under_a_post(self):
        response = self.client.post(
            "/posts/first-test/1/",
            {"username": "testuser2", "text": "testing the comment section"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/posts/first-test/1/")


class CreatePostViewTest(BaseSetUp):
    def test_that_the_view_url_exists(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/create-post/")
        self.assertEqual(response.status_code, 200)

    def test_that_the_view_url_exists_by_name(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("blogs:create_post"))
        self.assertEqual(response.status_code, 200)

    def test_that_the_view_requires_login(self):
        response = self.client.get("/create-post/")
        self.assertEqual(response.status_code, 302)

    def test_create_blog(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            "/create-post/",
            {
                "title": "test title",
                "text": "when testing, more is better",
                "source": "www.example.com/this-si",
            },
        )
        self.assertRedirects(response, "/")
        self.assertEqual(response.status_code, 302)

    def test_view_renders_correct_template(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/create-post/")
        self.assertTemplateUsed(response, "blogs/create_post.html")
        self.assertContains(response, "Create post")

    def test_that_unverified_authors_cannot_create_a_post(self):
        self.client.login(username="mantis", password="9wen3231")
        resp = self.client.get("/create-post/")
        response = self.client.post(
            "/create-post/",
            {
                "title": "test title",
                "text": "when testing, more is better",
                "source": "www.example.com/this-si",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            resp,
            "You are not a verified author. Only verified authors can create a post.",
        )


class EditPostViewTest(BaseSetUp):
    def test_that_the_view_url_exists(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/posts/first-test/1/edit-post/")
        self.assertEqual(response.status_code, 200)

    def test_that_the_view_url_exists_by_name(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("blogs:edit_post", args=["first-test", "1"]))
        self.assertEqual(response.status_code, 200)

    def test_that_the_view_requires_login(self):
        response = self.client.get("/posts/first-test/1/edit-post/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/users/login/?next=/posts/first-test/1/edit-post/"
        )

    def test_edit_blog(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            "/posts/first-test/1/edit-post/",
            {
                "title": "test title (edited)",
                "text": "when testing, more is better",
                "source": "www.example.com/try-keeping-this-simple",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/posts/test-title-edited/1/")

    def test_view_renders_correct_template(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/posts/first-test/1/edit-post/")
        self.assertTemplateUsed(response, "blogs/edit_post.html")
        self.assertContains(response, "Edit post")

    def test_that_unauthorized_users_cannot_edit_a_post(self):
        self.client.login(username="mantis", password="9wen3231")
        response = self.client.post(
            "/posts/first-test/1/edit-post/",
            {
                "title": "test title (dont't edit)",
                "text": "when testing, more is not better",
                "source": "www.example.com/this-si",
            },
        )
        self.assertEqual(response.status_code, 403)


class DeletePostViewTest(BaseSetUp):
    def test_that_the_view_url_exists(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/posts/first-test/1/delete-post/")
        self.assertEqual(response.status_code, 200)

    def test_that_the_view_url_exists_by_name(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(
            reverse("blogs:delete_post", args=["first-test", "1"])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_renders_correct_template(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get("/posts/first-test/1/delete-post/")
        self.assertTemplateUsed(response, "blogs/delete_post.html")
        self.assertContains(response, "Delete post")

    def test_that_the_view_requires_login(self):
        response = self.client.get("/posts/first-test/1/delete-post/")
        self.assertEqual(response.status_code, 302)

    def test_delete_post(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post("/posts/first-test/1/delete-post/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_that_user_cannot_delete_an_author_post(self):
        self.client.login(username="mantis", password="9wen3231")
        response = self.client.post("/posts/first-test/1/delete-post/")
        self.assertEqual(response.status_code, 403)
