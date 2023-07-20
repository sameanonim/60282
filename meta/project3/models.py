from django.contrib.auth.models import AbstractUser, Permission
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

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class Course(models.Model):
    title = models.CharField(_('название курса'), max_length=100)
    preview = models.ImageField(_('превью'), upload_to='course_previews/')
    description = models.TextField(_('описание курса'))
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('курс')
        verbose_name_plural = _('курсы')

class Lesson(models.Model):
    title = models.CharField(_('название урока'), max_length=100)
    description = models.TextField(_('описание урока'))
    preview = models.ImageField(_('превью'), upload_to='lesson_previews/')
    video_link = models.URLField(_('ссылка на видео'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='уроки')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = _('урок')
        verbose_name_plural = _('уроки')