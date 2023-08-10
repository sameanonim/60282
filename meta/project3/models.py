from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    email = models.EmailField(_('email адрес'), unique=True)
    phone = models.CharField(_('номер телефона'), max_length=15, blank=True, null=True)
    city = models.CharField(_('Город'), max_length=50, blank=True, null=True)
    avatar = models.ImageField(_('аватары'), upload_to='avatars/', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')

class Course(models.Model):
    title = models.CharField(_('название курса'), max_length=100)
    preview = models.ImageField(_('превью'), upload_to='course_previews/')
    description = models.TextField(_('описание курса'))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        subscriptions = Subscription.objects.filter(course=self)
        subscribed_users = [subscription.user.email for subscription in subscriptions if subscription.subscribed]
        subscribed_users_str = ', '.join(subscribed_users)
        return f"курс {self.title} - Подписаны: {subscribed_users_str}"
    
    def is_user_subscribed(self, user):
        try:
            Subscription.objects.get(user=user, course=self, subscribed=True)
            return True
        except Subscription.DoesNotExist:
            return False
    
    class Meta:
        verbose_name = _('курс')
        verbose_name_plural = _('курсы')

class Lesson(models.Model):
    title = models.CharField(_('название урока'), max_length=100)
    description = models.TextField(_('описание урока'))
    preview = models.ImageField(_('превью'), upload_to='lesson_previews/', null=True, blank=True)
    video_link = models.URLField(_('ссылка на видео'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='lessons')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = _('урок')
        verbose_name_plural = _('уроки')

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('пользователь'))
    payment_date = models.DateField(_('дата оплаты'))
    course_or_lesson = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='оплаченные_курсы_и_уроки',
        verbose_name=_('оплаченный курс или урок с указанием курса или урока')
    )
    amount = models.DecimalField(_('сумма оплаты'), max_digits=15, decimal_places=2)
    payment_method = models.CharField(
        _('способ оплаты'),
        max_length=15,
        choices=[('cash', 'наличные'), ('bank_transfer', 'перевод на счет')]
    )

    def __str__(self):
        return f"{self.user.email} - {self.course_or_lesson}"

    class Meta:
        verbose_name = _('платеж')
        verbose_name_plural = _('платежи')

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name=_('курс'))
    subscribed = models.BooleanField(_('подписан на обновления'), default=False)

    def __str__(self):
        return f"{self.user.email} - {self.course.title}"

    class Meta:
        verbose_name = _('подписка')
        verbose_name_plural = _('подписки')