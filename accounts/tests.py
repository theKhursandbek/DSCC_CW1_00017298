from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser

TEST_PASSWORD = "testpass123"  # NOSONAR — test-only credential


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
        user: CustomUser = CustomUser.objects.create_user(  # type: ignore[assignment]
            username="ageuser",
            email="ageuser@test.com",
            password=TEST_PASSWORD,
            age=25,
        )
        self.assertEqual(user.username, "ageuser")
        self.assertEqual(user.age, 25)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user: CustomUser = CustomUser.objects.create_superuser(  # type: ignore[assignment]
            username="superadmin",
            email="superadmin@test.com",
            password=TEST_PASSWORD,
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
