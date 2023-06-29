from rest_framework import serializers

from .models import Answer, Hint, Statistic, Tag, Task, Vocabular


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор модели Task."""

    class Meta:
        model = Task
        fields = ("task_index", "question", "answer", "image")
