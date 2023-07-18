from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Article, Tag, Comment


class BlogURLTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpassword"
        )
        self.tag1 = Tag.objects.create(slug='tag1', name='Tag 1')
        self.tag2 = Tag.objects.create(slug='tag2', name='Tag 2')
        self.article = Article.objects.create(
            title='Test Article',
            text='This is a test article',
            author='Test Author',
            count=5
        )
        self.article.tags.add(self.tag1, self.tag2)
        self.article.users.add(self.user)

        self.comment = Comment.objects.create(
            comment='Test Comment',
            user=self.user,
            article=self.article
        )
        self.client.login(username='testuser@example.com', password='testpassword')

    def test_list_view(self):
        url = reverse('blog:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_view(self):
        url = reverse('blog:create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_view(self):
        url = reverse('blog:update', kwargs={'pk': self.article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view(self):
        url = reverse('blog:delete', kwargs={'pk': self.article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_tags_view(self):
        url = reverse('blog:tags', kwargs={'slug': self.tag1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        url = reverse('blog:detail', kwargs={'pk': self.article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_like_view(self):
        url = reverse('blog:like', kwargs={'pk': self.article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
