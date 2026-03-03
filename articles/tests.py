from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Article, Comment


class ArticleModelTest(TestCase):
    """Test the Article model and its relationships."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        cls.user2 = get_user_model().objects.create_user(
            username="liker",
            password="testpass123",
        )
        cls.article = Article.objects.create(
            title="Test Article",
            summary="A short summary",
            body="<p>Full body content here.</p>",
            author=cls.user,
        )

    def test_article_creation(self):
        self.assertEqual(self.article.title, "Test Article")
        self.assertEqual(self.article.author.get_username(), "testuser")

    def test_article_str(self):
        self.assertEqual(str(self.article), "Test Article")

    def test_article_get_absolute_url(self):
        self.assertEqual(
            self.article.get_absolute_url(),
            f"/articles/{self.article.pk}/",
        )

    def test_article_like_m2m(self):
        """Verify M2M: multiple users can like an article."""
        self.article.likes.add(self.user, self.user2)
        self.assertEqual(self.article.total_likes(), 2)
        self.assertIn(self.user, self.article.likes.all())
        self.assertIn(self.user2, self.article.likes.all())

    def test_article_unlike(self):
        """Verify a user can unlike an article."""
        self.article.likes.add(self.user)
        self.assertEqual(self.article.total_likes(), 1)
        self.article.likes.remove(self.user)
        self.assertEqual(self.article.total_likes(), 0)

    def test_user_liked_articles_reverse(self):
        """Verify reverse M2M: a user can like multiple articles."""
        article2 = Article.objects.create(
            title="Second Article",
            body="<p>Body</p>",
            author=self.user,
        )
        self.article.likes.add(self.user2)
        article2.likes.add(self.user2)
        self.assertEqual(
            Article.objects.filter(likes=self.user2).count(), 2
        )


class CommentModelTest(TestCase):
    """Test the Comment model (many-to-one)."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="commenter",
            password="testpass123",
        )
        cls.article = Article.objects.create(
            title="Commented Article",
            body="<p>Body</p>",
            author=cls.user,
        )
        cls.comment = Comment.objects.create(
            article=cls.article,
            comment="Great post!",
            author=cls.user,
        )

    def test_comment_creation(self):
        self.assertEqual(str(self.comment), "Great post!")
        self.assertEqual(self.comment.article, self.article)

    def test_comment_many_to_one(self):
        """An article can have many comments."""
        Comment.objects.create(
            article=self.article,
            comment="Another comment",
            author=self.user,
        )
        self.assertEqual(Comment.objects.filter(article=self.article).count(), 2)


class ArticleListViewTest(TestCase):
    """Test the article list view."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="viewuser",
            password="testpass123",
        )
        Article.objects.create(
            title="View Test Article",
            body="<p>Body</p>",
            author=cls.user,
        )

    def test_article_list_status_code(self):
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)

    def test_article_list_template(self):
        response = self.client.get(reverse("article_list"))
        self.assertTemplateUsed(response, "article_list.html")

    def test_article_list_content(self):
        response = self.client.get(reverse("article_list"))
        self.assertContains(response, "View Test Article")


class ArticleDetailViewTest(TestCase):
    """Test the article detail view."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="detailuser",
            password="testpass123",
        )
        cls.article = Article.objects.create(
            title="Detail Test",
            body="<p>Detail body</p>",
            author=cls.user,
        )

    def test_article_detail_status_code(self):
        response = self.client.get(
            reverse("article_detail", args=[self.article.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_article_detail_template(self):
        response = self.client.get(
            reverse("article_detail", args=[self.article.pk])
        )
        self.assertTemplateUsed(response, "article_detail.html")


class ArticleCreateViewTest(TestCase):
    """Test that creating articles requires authentication."""

    def test_create_article_redirects_anonymous(self):
        response = self.client.get(reverse("article_new"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])


class ArticleLikeViewTest(TestCase):
    """Test the like/unlike toggle view (M2M)."""

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="likeuser",
            password="testpass123",
        )
        cls.article = Article.objects.create(
            title="Likeable Article",
            body="<p>Like me!</p>",
            author=cls.user,
        )

    def test_like_requires_login(self):
        response = self.client.get(
            reverse("article_like", args=[self.article.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_like_toggle(self):
        self.client.login(username="likeuser", password="testpass123")
        # Like
        response = self.client.get(
            reverse("article_like", args=[self.article.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.article.total_likes(), 1)
        # Unlike
        self.client.get(
            reverse("article_like", args=[self.article.pk])
        )
        self.assertEqual(self.article.total_likes(), 0)
