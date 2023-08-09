from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Course, Lesson, Subscription, User
from django.test import Client
from .serializers import MyTokenObtainPairSerializer
from django.test import override_settings

class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="testuser@mail.ru", password="testpass")
        self.course = Course.objects.create(title="Test Course", description="Test Description")
        self.lesson = Lesson.objects.create(title="Test Lesson", description="Test Description", video_link='https://www.youtube.com/watch?v=RY3ElwY4p0A', course=self.course)
    
    def test_create_lesson(self):
        url = '/lesson/create/'
        data = { "title": "Test Lesson", "description": "Test Description", "video_link": "https://www.youtube.com/watch?v=RY3ElwY4p0A", "course": self.course.pk }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Test Lesson')
        self.assertEqual(response.data['description'], 'Test Description')
        self.assertEqual(response.data['video_link'], 'https://www.youtube.com/watch?v=RY3ElwY4p0A')
    
    def test_read_lesson(self):
        url = f'/lesson/{self.lesson.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Lesson')
        self.assertEqual(response.data['description'], 'Test Description')
    
    def test_update_lesson(self):
        url = f'/lesson/update/{self.lesson.id}/'
        data = {"title": "Updated Test Lesson", "description": "Updated Test Description", "video_link": "https://www.youtube.com/watch?v=RY3ElwY4p0A", "course": self.course.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Test Lesson')
        self.assertEqual(response.data['description'], 'Updated Test Description')
        self.assertEqual(response.data['video_link'], 'https://www.youtube.com/watch?v=RY3ElwY4p0A')
    
    def test_delete_lesson(self):
        url = f'/lesson/delete/{self.lesson.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        super().tearDown()
    
class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User(email='test@test.ru', phone='111111111', city='Mscow', is_superuser=True, is_staff=True,
                         is_active=True)
        self.user.set_password('123QWE456RTY')
        self.user.save()
        response = self.client.post(
            '/token/',
            {"email": "test@test.ru", "password": "123QWE456RTY"}
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.course = Course.objects.create(title='test', description='test')

    def test_subscription_create(self):
        response = self.client.post('/subscriptions/create/',
                                    {'course_id': self.course.id, 'user': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_delete(self):
        self.test_subscription_create()
        response = self.client.delete(f'/subscriptions/delete/?course_id={self.course.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        super().tearDown()