from django.contrib.admin import ModelAdmin, register

from .models import Task, VocabularJokes, VocabularReactions


@register(Task)
class TaskAdmin(ModelAdmin):
    pass


@register(VocabularReactions)
class ReactionsAdmin(ModelAdmin):
    pass


@register(VocabularJokes)
class JokesAdmin(ModelAdmin):
    pass
