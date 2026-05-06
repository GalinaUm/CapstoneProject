from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .filters import AdFilter
from .models import Ad, Review
from .paginators import AdPagination
from .permissions import IsOwnerOrAdmin
from .serializers import AdDetailSerializer, AdSerializer, ReviewSerializer


class AdViewSet(ModelViewSet):
    pagination_class = AdPagination
    queryset = Ad.objects.all()

    filter_backends = (DjangoFilterBackend,)
    filterset_class = AdFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]

        return [IsAuthenticated(), IsOwnerOrAdmin()]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        ad_id = self.kwargs.get("ad_id")
        if ad_id:
            return Review.objects.filter(ad_id=ad_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        ad_id = self.kwargs.get("ad_id")

        if Review.objects.filter(ad_id=ad_id, author=self.request.user).exists():
            raise ValidationError(
                {"detail": "Вы уже оставляли отзыв на это объявление."}
            )

        serializer.save(
            author=self.request.user,
            ad_id=ad_id,
        )
