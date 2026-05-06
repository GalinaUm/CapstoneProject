import pytest
from django.urls import reverse
from rest_framework import status

from users.models import User


@pytest.mark.django_db
class TestUserAuth:
    def test_user_registration(self, api_client):
        url = reverse("users:user_create")

        data = {
            "email": "new@test.com",
            "password": "newpassword123!",
            "first_name": "Марсель",
            "last_name": "Умерзаков",
            "phone": "+79281889581",
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email="new@test.com").exists()

        user = User.objects.get(email="new@test.com")

        assert user.check_password("newpassword123!")
        assert user.role == User.USER

    def test_user_cannot_register_as_admin(self, api_client):
        url = reverse("users:user_create")

        data = {
            "email": "hacker@test.com",
            "password": "newpassword123!",
            "role": User.ADMIN,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED

        user = User.objects.get(email="hacker@test.com")

        assert user.role == User.USER

    def test_user_login_by_jwt(self, api_client, user):
        url = reverse("users:login")

        response = api_client.post(
            url,
            {"email": "user@test.com", "password": "userpassword123"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_get_me_authenticated(self, auth_client, user):
        url = reverse("users:user_me")

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == user.email

    def test_get_me_anonymous_denied(self, api_client):
        url = reverse("users:user_me")

        response = api_client.get(url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_can_change_password(self, auth_client, user):
        url = reverse("users:user_me")

        response = auth_client.patch(
            url,
            {"password": "newstrongpassword123!"},
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()

        assert user.check_password("newstrongpassword123!")

    def test_password_reset_request_existing_email(
        self, api_client, user, settings, mocker
    ):
        settings.PASSWORD_RESET_CONFIRM_URL = "http://test/reset/{uid}/{token}/"

        mocked_send_mail = mocker.patch("users.views.send_mail")

        url = reverse("users:reset_password")

        response = api_client.post(
            url,
            {
                "email": user.email,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "Инструкции отправлены на почту."
        mocked_send_mail.assert_called_once()

    def test_password_reset_request_unknown_email_does_not_send_mail(
        self, api_client, settings, mocker
    ):
        settings.PASSWORD_RESET_CONFIRM_URL = "http://test/reset/{uid}/{token}/"

        mocked_send_mail = mocker.patch("users.views.send_mail")

        url = reverse("users:reset_password")

        response = api_client.post(
            url,
            {
                "email": "unknown@test.com",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        mocked_send_mail.assert_not_called()
