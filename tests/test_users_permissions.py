import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUsersPermissions:
    def test_regular_user_cannot_get_user_list(self, auth_client):
        url = reverse("users:user_list")

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_get_users_list(self, admin_client):
        url = reverse("users:user_list")

        response = admin_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_user_can_update_own_profile(self, auth_client, user):
        url = reverse("users:user_me")

        response = auth_client.patch(
            url,
            {
                "first_name": "Updated",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()

        assert user.first_name == "Updated"

    def test_user_cannot_update_other_user(self, auth_client, other_user):
        url = reverse("users:user_update", args=[other_user.id])

        response = auth_client.patch(
            url,
            {
                "first_name": "Hack",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_other_user(self, admin_client, other_user):
        url = reverse("users:user_update", args=[other_user.pk])

        response = admin_client.patch(
            url,
            {
                "first_name": "Admin updated",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK

        other_user.refresh_from_db()

        assert other_user.first_name == "Admin updated"

    def test_user_cannot_delete_other_user(self, auth_client, other_user):
        url = reverse("users:user_delete", args=[other_user.pk])

        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_cannot_delete_other_user(self, admin_client, other_user):
        url = reverse("users:user_delete", args=[other_user.pk])

        response = admin_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
