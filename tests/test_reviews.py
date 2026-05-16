import pytest
from django.urls import reverse
from rest_framework import status

from ads.models import Review


@pytest.mark.django_db
class TestReview:
    def test_reviews_list_available_for_anonymous(self, api_client, ad, review):
        url = reverse("ads:review-list", kwargs={"ad_id": ad.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK

    def test_authenticated_user_can_create_review(self, auth_client, ad, user):
        url = reverse("ads:review-list", kwargs={"ad_id": ad.pk})
        data = {
            "text": "Excellent ad",
            "rating": 5,
        }

        response = auth_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED

        created_review = Review.objects.get(text="Excellent ad")

        assert created_review.text == "Excellent ad"
        assert created_review.rating == 5
        assert created_review.ad == ad
        assert created_review.author == user

    def test_anonymous_user_cannot_create_review(self, api_client, ad):
        url = reverse("ads:review-list", kwargs={"ad_id": ad.pk})
        data = {
            "text": "Anonymous review",
            "rating": 5,
        }

        response = api_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_review_rating_cannot_be_less_than_1(self, auth_client, ad):
        url = reverse("ads:review-list", kwargs={"ad_id": ad.pk})
        data = {
            "text": "Bad rating",
            "rating": 0,
        }

        response = auth_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_review_rating_cannot_be_more_than_5(self, auth_client, ad):
        url = reverse("ads:review-list", kwargs={"ad_id": ad.pk})
        data = {
            "text": "Bad rating",
            "rating": 6,
        }

        response = auth_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_cannot_create_second_review_for_same_ad(
        self, auth_client, ad, review
    ):
        url = reverse("ads:review-list", kwargs={"ad_id": ad.pk})
        data = {
            "text": "Second review",
            "rating": 4,
        }

        response = auth_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_review_author_is_read_only(self, auth_client, ad, user, other_user):
        url = reverse("ads:review-list", kwargs={"ad_id": ad.pk})
        data = {
            "text": "Review with fake author",
            "rating": 5,
            "author": other_user.email,
        }

        response = auth_client.post(url, data, format="json")

        assert response.status_code == status.HTTP_201_CREATED

        created_review = Review.objects.get(text="Review with fake author")

        assert created_review.author == user
        assert created_review.author != other_user
