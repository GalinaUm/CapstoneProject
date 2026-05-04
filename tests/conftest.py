import pytest
from rest_framework.test import APIClient

from users.models import User
from ads.models import Ad, Review


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@test.com",
        password="userpassword123",
    )

@pytest.fixture
def other_user(db):
    return User.objects.create_user(
        email="other@test.com",
        password="otherpassword123",
    )

@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        email="admin@test.com",
        password="adminpassword123",
    )

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def admin_client(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    return api_client

@pytest.fixture
def ad(user):
    return Ad.objects.create(
        title="Test ad",
        price=1000,
        description="Test description",
        author=user,
    )

@pytest.fixture
def other_ad(other_user):
    return Ad.objects.create(
        title="Other ad",
        price=5000,
        description="Other description",
        author=other_user,
    )

@pytest.fixture
def review(user, ad):
    return Review.objects.create(
        text="Good review",
        author=user,
        ad=ad,
        rating=5,
    )