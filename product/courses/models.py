from django.db import models
from django.core.exceptions import PermissionDenied


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость',
        default=0.00
    )
    
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        if not self.author.is_teacher:
            raise PermissionDenied("Только преподаватель может создавать уроки.")
        super().save(*args, **kwargs)    

    def __str__(self):
        return self.title


# В уроках тоже надо проверку сделать на тот кто создаёт, это должен быть учитель, при чём тот кто создал данный курс
class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс',
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    name = models.CharField(max_length=100, verbose_name='Название группы')
    
    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
