from django.contrib.admin import ModelAdmin, register

from .models import Task, VocabularReactions, VocabularJokes


@register(Task)
class TaskAdmin(ModelAdmin):
    pass


@register(VocabularReactions)
class ReactionsAdmin(ModelAdmin):
    pass


@register(VocabularJokes)
class JokesAdmin(ModelAdmin):
    pass
