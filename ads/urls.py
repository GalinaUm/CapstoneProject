from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AdViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename="ads")

urlpatterns = [
    path('', include(router.urls)),
    path('ads/<int:ad_id>/reviews/',
         ReviewViewSet.as_view({'get': 'list', 'post': 'create'}),
         name="review-list",
    ),
    path('ads/<int:ad_id>/reviews/<int:pk>/',
         ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
        name="review-detail",
    ),
]