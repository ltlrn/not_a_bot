from rest_framework.viewsets import ModelViewSet

from .models import Task, VocabularJokes, VocabularReactions
from .serializers import JokesSerializer, ReactionsSerializer, TaskSerializer


class TaskViewSet(ModelViewSet):
    """Вьюсет для заданий."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class JokesViewSet(ModelViewSet):
    """Вьюсет для шуток."""

    queryset = VocabularJokes.objects.all()
    serializer_class = JokesSerializer


class ReactionsViewSet(ModelViewSet):
    """Вьюсет для реакций."""

    queryset = VocabularReactions.objects.all()
    serializer_class = ReactionsSerializer
