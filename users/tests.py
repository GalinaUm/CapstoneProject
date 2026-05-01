import pytest
from django.urls import reverse
from rest_framework import status
from users.models import User


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def test_user(db):
    return User.objects.create_user(email="test@test.com", password="testpassword123")


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(email="admin@test.com", password="adminpassword123")


@pytest.fixture
def user_token(api_client, test_user):
    url = reverse("users:login")
    response = api_client.post(url, {"email": "test@test.com", "password": "testpassword123"})
    return response.data["access"]


@pytest.mark.django_db
class TestUsers:

    def test_registration(self, api_client):
        url = reverse("users:user_create")
        data = {"email": "new@test.com", "password": "newpassword123!"}
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_me(self, api_client, user_token):
        url = reverse("users:user_me")
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == "test@test.com"

    def test_admin_list_access(self, api_client, user_token, admin_user):
        url = reverse("users:user_list")

        # Проверка обычного юзера
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        assert api_client.get(url).status_code == status.HTTP_403_FORBIDDEN

        # Проверка админа
        login_url = reverse("users:login")
        admin_token = api_client.post(login_url, {"email": admin_user.email, "password": "adminpassword123"}).data[
            "access"]
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
        assert api_client.get(url).status_code == status.HTTP_200_OK

    def test_owner_permission_denied(self, api_client, user_token, db):
        other_user = User.objects.create_user(email="other@test.com", password="password")
        url = reverse("users:user_update", args=[other_user.id])

        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        response = api_client.patch(url, {"first_name": "Hack"})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_password_reset_request(self, api_client, test_user):
        url = reverse("users:reset_password")
        response = api_client.post(url, {"email": test_user.email})
        assert response.status_code == status.HTTP_200_OK
