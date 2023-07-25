from django.core.management.base import BaseCommand
from project3.models import User, Course, Payment

class Command(BaseCommand):
    help = 'Добавить данные о платежах в базу данных'

    def handle(self, *args, **kwargs):
        # Ваш код для добавления данных о платежах здесь
        try:
            user1 = User.objects.get(id=2)
            course1 = Course.objects.get(id=1)

            Payment.objects.create(
                user=user1,
                payment_date='2023-07-25',
                course_or_lesson=course1,
                amount=100.50,
                payment_method='cash'
            )

            self.stdout.write(self.style.SUCCESS('Данные о платежах успешно добавлены!'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Пользователь не найден. Убедитесь, что пользователь с указанным id существует в базе данных.'))
        except Course.DoesNotExist:
            self.stdout.write(self.style.ERROR('Курс не найден. Убедитесь, что курс с указанным id существует в базе данных.'))