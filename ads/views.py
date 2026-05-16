from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import AdFilter
from .models import Ad, Review
from .paginators import AdPagination
from .permissions import IsOwnerOrAdmin
from .serializers import AdDetailSerializer, AdSerializer, ReviewSerializer


class AdViewSet(ModelViewSet):
    """
    ViewSet для работы с объявлениями.

    Поддерживает:
    - список объявлений
    - создание
    - получение
    - обновление
    - удаление
    """

    pagination_class = AdPagination
    queryset = Ad.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    def get_serializer_class(self):
        """
        Возвращает serializer в зависимости от action.

        retrieve -> AdDetailSerializer
        остальные -> AdSerializer
        """
        if self.action == "retrieve":
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        """Автоматически назначает автора объявления."""
        serializer.save(author=self.request.user)

    def get_permissions(self):
        """
        Возвращает permissions для action.

        list:
            доступен всем пользователям

        остальные:
            только авторизованным
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [IsAuthenticated(), IsOwnerOrAdmin()]


class ReviewViewSet(ModelViewSet):
    """
    ViewSet для работы с отзывами.

    Доступ:
    - list/retrieve: доступны всем пользователям
    - create/update/delete: только авторизованным
    - update/delete: только автор отзыва или администратор
    """

    serializer_class = ReviewSerializer

    def get_queryset(self):
        """
        Возвращает queryset отзывов.

        Если передан ad_id:
            возвращаются отзывы конкретного объявления.
        """
        ad_id = self.kwargs.get("ad_id")
        if ad_id:
            return Review.objects.filter(ad_id=ad_id)
        return Review.objects.all()

    def get_permissions(self):
        """
        Возвращает permissions в зависимости от action.

        Читать отзывы могут все.
        Создавать, редактировать и удалять могут только авторизованные пользователи.
        """

        if self.action in ["list", "retrieve"]:
            return [AllowAny()]

        return [IsAuthenticated(), IsOwnerOrAdmin()]

    def perform_create(self, serializer):
        """
        Создает отзыв и автоматически назначает автора и объявление.

        Также запрещает пользователю оставлять второй отзыв
        на одно и то же объявление.
        """

        ad_id = self.kwargs.get("ad_id")

        if Review.objects.filter(ad_id=ad_id, author=self.request.user).exists():
            raise ValidationError(
                {"detail": "Вы уже оставляли отзыв на это объявление."}
            )

        serializer.save(
            author=self.request.user,
            ad_id=ad_id,
        )
