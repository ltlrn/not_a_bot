from rest_framework import serializers

from .models import Task, VocabularJokes, VocabularReactions


class TaskSerializer(serializers.ModelSerializer):
    """Сериализатор модели Task."""

    class Meta:
        model = Task
        fields = ("task_index", "question", "answer")


class ReactionsSerializer(serializers.ModelSerializer):
    """Сериализатор модели VocabularReactions."""

    class Meta:
        model = VocabularReactions
        fields = ("mistake_light", "mistake_hard", "mistake_critical", "reaction")


class JokesSerializer(serializers.ModelSerializer):
    """Сериализатор модели VocabularJokes."""

    class Meta:
        model = VocabularJokes
        fields = ("polite_joke", "stupid_joke", "sarcasm")
