from rest_framework import serializers

from .models import Ad, Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    author = serializers.ReadOnlyField(source="author.email")
    ad = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ("id", "text", "author", "ad", "rating", "created_at")


class AdSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор объявлений.

    Используется для списка объявлений.
    """

    author = serializers.ReadOnlyField(source="author.email")
    reviews_count = serializers.IntegerField(source="reviews.count", read_only=True)

    class Meta:
        model = Ad
        fields = (
            "id",
            "image",
            "title",
            "price",
            "description",
            "author",
            "created_at",
            "reviews_count",
        )


class AdDetailSerializer(serializers.ModelSerializer):
    """
    Детальный сериализатор объявления.

    Включает описание и список отзывов.
    """

    author = serializers.ReadOnlyField(source="author.email")
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Ad
        fields = (
            "id",
            "image",
            "title",
            "price",
            "description",
            "author",
            "created_at",
            "reviews",
        )
