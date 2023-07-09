from rest_framework import serializers

from .models import Answer, Hint, Statistic, Tag, Task, Vocabular


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор модели Task."""

    class Meta:
        model = Task
        fields = (
            "id",
            "task_index",
            "question", 
            "answer", 
            "image"
        )


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор модели Answer."""

    class Meta:
        model = Answer
        fields = ("task_index", "question", "answer", "image")


class HintSerializer(serializers.ModelSerializer):
    """Сериализатор модели Hint."""

    class Meta:
        model = Hint
        fields = ("task_index", "question", "answer", "image")


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели Tag."""

    class Meta:
        model = Task
        fields = ("id", "name", "slug")


class VocSerializer(serializers.ModelSerializer):
    """Сериализатор модели Vocabular."""
    # tag = TagSerializer(read_only=True)    

    class Meta:
        model = Vocabular
        fields = ("id", "sentence", "tag")


class StatSerializer(serializers.ModelSerializer):
    """Сериализатор модели Statistic."""

    class Meta:
        model = Statistic
        fields = ("task_index", "question", "answer", "image")
