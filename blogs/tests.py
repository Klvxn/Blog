from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from blogs.models import Author, BlogPost, Comment
from django.contrib.auth import get_user_model


# Create your tests here.
class HomepageTest(TestCase):
   
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Blog')
    
    def test_homepage_exists_by_name(self):
        response = self.client.get(reverse('blogs:index'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'blogs/index.html')

    def test_search_bar_is_in_homepage(self):
        response = self.client.get('/')
        self.assertContains(response, 'Search')
        self.assertTemplateUsed(response, 'blogs/index.html')


class AuthorModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='testpassword')
        self.author = Author.objects.create(user=self.user, firstname='test', lastname='user', email='testuser@blogs.xo')
        return super().setUp()

    def test_string_representation(self):
        author = self.author
        self.assertEqual(str(author.firstname), 'test', author.firstname)

    def test_get_absolute_url(self):
        self.assertEqual(self.author.get_absolute_url(), '/author/test-user/')

    def test_author_detail_view(self):
        response = self.client.get('/author/test-user/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/authorpage.html')

    def test_authors_view(self):
        response = self.client.get('/authors/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/authorspage.html')
        self.assertContains(response, 'Authors')

    def test_become_an_author_page(self):
        response = self.client.get('/become-an-author/')
        self.assertRedirects(response, '/users/login/?next=/become-an-author/')
        self.assertEqual(response.status_code, 302)

    def test_edit_author_profile(self):
        get_response = self.client.get('/author/test-user/edit-profile/')
        post_response = self.client.post('/author/test-user/edit-profile/', {'bio':'i love running tests'})
        self.assertRedirects(get_response , '/users/login/?next=/author/test-user/edit-profile/')
        self.assertRedirects(post_response , '/users/login/?next=/author/test-user/edit-profile/')
        self.assertEqual(get_response.status_code, post_response.status_code, 302)


class BlogPostModelTest(TestCase):

    title = 'test post'
    text = 'running tests with pytest-django'
    slug = slugify(title)

    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='testpassword')
        self.author = Author.objects.create(user=self.user, firstname='test', lastname='user', email='testuser@blogs.xo')
        self.blog = BlogPost.objects.create(title=self.title, text=self.text, slug=self.slug, author=self.author)
        return super().setUp()

    def test_string_representation(self):
        post = self.blog
        self.assertEqual(f'{post.title} by {post.author}', 'test post by test')

    def test_get_absolute_url(self):
        self.assertEqual(self.blog.get_absolute_url(), '/post/test-post/1/')

    def test_blogpost_detail_view(self):
        response = self.client.get('/post/test-post/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blogs/post_detail.html')
        self.assertContains(response, 'test post')

    def test_date_of_blogpost(self):
        current_date = timezone.now()
        self.assertEqual(self.blog.date_added, current_date)

    def test_slug_of_blogpost(self):
        test_slug = 'test-post'
        self.assertEqual(self.blog.slug, test_slug)

    def test_author_of_blogpost(self):
        test_author = 'test'
        self.assertEqual(self.blog.author.firstname, test_author)

    def test_add_blogpost(self):
        response = self.client.post('/create-post/', {
            'title':'test title',
            'text':'when testing, more is better',
            'author':self.author})
        self.assertRedirects(response, '/users/login/?next=/create-post/')
        self.assertEqual(response.status_code, 302)

    def test_edit_blogpost(self):
        response = self.client.post('/post/test-post/1/edit-post', {'title':'don\'t stop testing'})
        self.assertEqual(response.status_code, 301)

    def test_delete_blogpost(self):
        response = self.client.post('/post/test-post/1/delete-post')
        self.assertEqual(response.status_code, 301)


class CommentModelTest(TestCase):

    title = 'test post'
    text = 'running tests with pytest-django'
    slug = slugify(title)

    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='testpassword')
        self.author = Author.objects.create(user=self.user, firstname='test', lastname='user', email='testuser@blogs.xo')
        self.blog = BlogPost.objects.create(title=self.title, text=self.text, slug=self.slug, author=self.author)
        self.comment = Comment.objects.create(post=self.blog, username='testuser2', text='test the comment section')
        return super().setUp()

    def test_string_representation(self):
        comment = self.comment
        self.assertEqual(f'{self.comment.text} by {self.comment.username}', 'test the comment section by testuser2')

    def test_comment_section_exists_in_a_post(self):
        response = self.client.get('/post/test-post/1/')
        self.assertContains(response, 'Comments')

    def test_post_a_comment_under_a_blogpost(self):
        response = self.client.post('/post/test-post/1/', {'username':'testuser2', 'text':'testing the comment section'})
        self.assertRedirects(response, '/post/test-post/1/')
        self.assertEqual(response.status_code, 302)

    def test_date_of_comment(self):
        date = timezone.now().date()
        self.assertEqual(self.comment.date_created.date(), date)
