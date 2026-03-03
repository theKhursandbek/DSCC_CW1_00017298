from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class SignUpPageTest(TestCase):
    """Test the signup page."""

    def test_signup_page_status_code(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_template(self):
        response = self.client.get(reverse("signup"))
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_signup_page_contains_form(self):
        response = self.client.get(reverse("signup"))
        self.assertContains(response, "csrfmiddlewaretoken")


class CustomUserModelTest(TestCase):
    """Test the CustomUser model."""

    def test_create_user_with_age(self):
        user = get_user_model().objects.create_user(
            username="ageuser",
            password="testpass123",
            age=25,
        )
        self.assertEqual(user.username, "ageuser")
        self.assertEqual(user.age, 25)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = get_user_model().objects.create_superuser(
            username="superadmin",
            password="testpass123",
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
