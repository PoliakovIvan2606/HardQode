from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    is_teacher = models.BooleanField(default=False, verbose_name='Преподаватель')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )
    


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='balance',
        verbose_name='Пользователь',
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Баланс',
        default=1000.00 
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее обновление',
    )

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValueError("Баланс не может быть отрицательным.")
        super().save(*args, **kwargs)

# При покупки курса пользователь добавляется в таблицу ссылой на данный курс 
class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь',
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Курс',
    )
    
    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user} - {self.course}'


