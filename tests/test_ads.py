import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import Ad

@pytest.mark.django_db
class TestAds:
    def test_ads_list_available_for_anonymous(self, api_client, ad):
        url = reverse('ads:ads-list')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_user_can_create_ad(self, auth_client, user):
        url = reverse('ads:ads-list')

        data = {
            'title': 'New ad',
            'price': 2500,
            'description': 'New description',
        }

        response = auth_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        created_ad = Ad.objects.get(title='New ad')

        assert created_ad.title == 'New ad'
        assert created_ad.price == 2500
        assert created_ad.description == 'New description'
        assert created_ad.author == user

    def test_anonymous_user_cannot_create_ad(self, api_client):
        url = reverse('ads:ads-list')

        data = {
            'title': 'New ad',
            'price': 2500,
            'description': 'New description',
        }

        response = api_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_owner_can_update_own_ad(self, auth_client, ad):
        url = reverse('ads:ads-detail', args=[ad.pk])

        response = auth_client.patch(
            url,
            {'title': 'Updated title'},
            format='json'
        )

        assert response.status_code == status.HTTP_200_OK

        ad.refresh_from_db()

        assert ad.title == 'Updated title'

    def test_owner_cannot_update_other_user_ad(self, auth_client, other_ad):
        url = reverse('ads:ads-detail', args=[other_ad.pk])

        response = auth_client.patch(
            url,
            {'title': 'Hack title'},
            format='json',
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update_any_ad(self, admin_client, other_ad):
        url = reverse('ads:ads-detail', args=[other_ad.pk])

        response = admin_client.patch(
            url,
            {'title': 'Admin title'},
            format='json',
        )

        assert response.status_code == status.HTTP_200_OK

        other_ad.refresh_from_db()

        assert other_ad.title == 'Admin title'

    def test_owner_can_delete_own_ad(self, auth_client, ad):
        url = reverse('ads:ads-detail', args=[ad.pk])

        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Ad.objects.filter(pk=ad.pk).exists()

    def test_user_cannot_delete_other_user_ad(self, auth_client, other_ad):
        url = reverse('ads:ads-detail', args=[other_ad.pk])

        response = auth_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert Ad.objects.filter(pk=other_ad.pk).exists()

    def test_ad_list_contains_reviews_count(self, api_client, ad, review):
        url = reverse('ads:ads-list')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

        result = response.data['results'] if "results" in response.data else response.data
        first_item = result[0]

        assert first_item['reviews_count'] == 1
        assert "reviews_count" in first_item

    def test_ad_retrieve_uses_detail_serializer_with_reviews(self, auth_client, ad, review):
        url = reverse('ads:ads-detail', args=[ad.pk])

        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "description" in response.data
        assert "reviews" in response.data
        assert len(response.data['reviews']) == 1

    def test_filter_ads_by_title(self, api_client, ad, other_ad):
        url = reverse('ads:ads-list')
        response = api_client.get(url, {'title': 'Test'})

        assert response.status_code == status.HTTP_200_OK

        result = response.data['results'] if "results" in response.data else response.data
        titles = [item["title"] for item in result]

        assert "Test ad" in titles
        assert "Other ad" not in titles

    def test_filter_ads_by_min_price(self, api_client, ad, other_ad):
        url = reverse('ads:ads-list')

        response = api_client.get(url, {"min_price": 2000})

        assert response.status_code == status.HTTP_200_OK

        result = response.data['results'] if "results" in response.data else response.data
        titles = [tem["title"] for tem in result]

        assert "Test ad" not in titles
        assert "Other ad" in titles

    def test_filter_ads_by_max_price(self, api_client, ad, other_ad):
        url = reverse('ads:ads-list')

        response = api_client.get(url, {"max_price": 2000})
        assert response.status_code == status.HTTP_200_OK

        result = response.data['results'] if "results" in response.data else response.data
        titles = [item["title"] for item in result]

        assert "Test ad" in titles
        assert "Other ad" not in titles

    def test_filter_ads_by_author_email(self, api_client, ad):
        url = reverse('ads:ads-list')

        response = api_client.get(url, {"email": "user@test.com"})

        assert response.status_code == status.HTTP_200_OK

        results = response.data['results'] if "results" in response.data else response.data

        assert len(results) == 1
        assert results[0]["author"] == "user@test.com"

    def test_ads_pagination_default_page_size_is_4(self, api_client, user):
        for index in range(6):
            Ad.objects.create(
                title=f"Ad {index}",
                price=100 + index,
                author=user,
            )
        url = reverse('ads:ads-list')

        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert "results" in response.data
        assert len(response.data['results']) == 4

    def test_ads_pagination_page_size_query_param(self, api_client, user):
        for index in range(6):
            Ad.objects.create(
                title=f"Ad {index}",
                price=100 + index,
                author=user,
            )

        url = reverse('ads:ads-list')

        response = api_client.get(url, {'page_size': 2})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

