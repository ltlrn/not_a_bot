from django.contrib.admin import ModelAdmin, register

from .models import Task


@register(Task)
class TaskAdmin(ModelAdmin):
    pass
