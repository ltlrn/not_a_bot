from django.db import models


class Task(models.Model):
    """Модель тестового задания, содержит вопрос в виде
    изображения и правильный вариант ответа.
    """

    task_index = models.CharField("индекс")
    question = models.TextField("вопрос")
    image = models.ImageField("картинка", upload_to="tasks/")
    answer = models.IntegerField("правильный ответ")

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.task_index


class VocabularReactions(models.Model):
    """Словарный запас бота: реакции."""

    mistake_light = models.CharField(
        "небольшая ошибка", unique=True
    )  # may be unlimited with Postgres
    mistake_hard = models.CharField("ошибка", unique=True)
    mistake_critical = models.CharField("грубая ошибка", unique=True)
    reaction = models.CharField("реакция", unique=True)

    class Meta:
        verbose_name = "Набор реакций"
        verbose_name_plural = "Реакции"


class VocabularJokes(models.Model):
    """Словарный запас бота: шутки."""

    polite_joke = models.CharField("вежливая шутка", unique=True)
    stupid_joke = models.CharField("тупая шутка", unique=True)
    sarcasm = models.CharField("сарказм", unique=True)

    class Meta:
        verbose_name = "Набор шуток"
        verbose_name_plural = "Шутки"


class VocabularFacts(models.Model):
    """Словарный запас бота: факты."""

    pass


class VocabularHints(models.Model):
    """Словарный запас бота: подсказки."""

    pass
