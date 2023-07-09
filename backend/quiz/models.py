from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Task(models.Model):
    """Модель тестового задания, содержит вопрос в виде
    изображения и правильный вариант ответа.
    """

    variant = models.CharField("вариант")
    question_text = models.TextField("вопрос", blank=True)
    question_image = models.ImageField("картинка", upload_to="tasks/")

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    def __str__(self):
        return self.variant


class Answer(models.Model):
    """Модель вариантов ответов, ассоциированых с каждым заданием."""

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="answers", verbose_name="задания"
    )

    text = models.CharField("текст ответа")
    is_correct = models.BooleanField("правильный")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return self.text


class Hint(models.Model):
    """Модель подсказок, доступных для заданий."""

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="hints", verbose_name="задания"
    )

    text = models.CharField("текст подсказки")

    class Meta:
        verbose_name = "Подсказка"
        verbose_name_plural = "Подсказки"

    def __str__(self):
        return self.text


class Statistic(models.Model):
    """Статистика выполнения заданий."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stats", verbose_name="статистика"
    )

    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name="stats", verbose_name="статистика"
    )

    solved_at = models.DateTimeField(
        "решение зафиксировано", auto_now_add=True, db_index=True
    )

    is_correct = models.BooleanField("решение верно")
    with_hint = models.BooleanField("подсказка взята")
    solving_time = models.DateTimeField("время решения")

    class Meta:
        verbose_name = "Статистика"

    def __str__(self):
        return self.solved_at


class Tag(models.Model):
    """Теги для словарного запаса."""

    name = models.CharField("тег", max_length=200)

    slug = models.SlugField(
        "слаг тега",
        max_length=200,
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Vocabular(models.Model):
    """Словарный запас бота."""

    sentence = models.TextField("высказывание")
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, verbose_name="тег", related_name="tags"
    )

    class Meta:
        verbose_name = "Фраза"
        verbose_name_plural = "Фразы"

    def __str__(self):
        return self.sentence[:50]
