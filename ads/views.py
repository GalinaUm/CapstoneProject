from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .paginators import AdPagination
from .models import Ad, Review
from .serializers import AdSerializer, AdDetailSerializer, ReviewSerializer
from .filters import AdFilter

from .permissions import IsOwnerOrAdmin
from rest_framework.permissions import AllowAny, IsAuthenticated

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
        serializer.save(
            author=self.request.user,
            ad_id=ad_id,
            )