from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .models import Ad, Review
from .serializers import AdSerializer, AdDetailSerializer, ReviewSerializer

class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AdDetailSerializer
        return AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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