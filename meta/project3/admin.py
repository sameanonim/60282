from django.contrib import admin
from project3.models import User, Course, Lesson, Payment

# Register your models here.
admin.site.register(User)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Payment)