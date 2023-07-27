from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Article, Tag, Comment


class ArticleModelTestCase(TestCase):
    # setUp: method毎に行われる
    # setUpTestData: class毎に行われる
    @classmethod
    def setUpTestData(self):
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
    
    def test_article_model_str(self):
        # __str__の検証
        self.assertEqual(str(self.article), 'Test Article')
    
    def test_article_model_defaults(self):
        # 設定項目のチェック
        self.assertEqual(self.article.title, 'Test Article')
        self.assertEqual(self.article.text, 'This is a test article')
        self.assertEqual(self.article.image.name, '')
        self.assertEqual(self.article.author, 'Test Author')
        self.assertEqual(self.article.count, 5)
        self.assertEqual(self.article.tags.count(), 2)
        self.assertEqual(self.article.tags.first(), self.tag1)
        self.assertEqual(self.article.tags.last(), self.tag2)
        self.assertEqual(self.article.users.count(), 1)
        self.assertEqual(self.article.users.first(), self.user)
    
    def text_comment_model_str(self):
        self.assertEqual(str(self.comment), 'Test Comment')
    
    def test_comment_model_defaults(self):
        self.assertEqual(self.comment.comment, 'Test Comment')
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.article, self.article)

    def test_comment_model_created_at(self):
        self.assertIsNotNone(self.comment.created_at)


class TagModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(slug='test-tag', name='Test Tag')

    def test_tag_model_str(self):
        self.assertEqual(str(self.tag), 'test-tag')

    def test_tag_model_defaults(self):
        self.assertEqual(self.tag.slug, 'test-tag')
        self.assertEqual(self.tag.name, 'Test Tag')
