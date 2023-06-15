from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import JokesViewSet, ReactionsViewSet, TaskViewSet

router = DefaultRouter()

router.register(r"tasks", TaskViewSet, "tasks")
router.register(r"jokes", JokesViewSet, "jokes")
router.register(r"reactions", ReactionsViewSet, "reactions")

urlpatterns = [
    path("", include(router.urls)),
]
