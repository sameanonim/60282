from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Course, Lesson, Subscription, User
from django.test import Client

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
        self.course.delete()
        self.lesson.delete()
        self.user.delete()
        del self.course
        del self.lesson
        del self.client
    
class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email="testuser@mail.ru", password="testpass")
        self.course = Course.objects.create(title="Test Course", description="Test Description")

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        url = '/subscriptions/create/'
        csrf_client = Client()
        csrf_token = csrf_client.cookies['csrftoken'].value
        print(csrf_token)
        data = {'course_id': self.course.id, 'csrfmiddlewaretoken': csrf_token}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsubscribe_from_course(self):
        self.client.force_authenticate(user=self.user)
        subscription = Subscription.objects.create(user=self.user, course=self.course, subscribed=True)
        url = f'/subscriptions/delete/{subscription.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        self.course.delete()
        self.user.delete()
        del self.course
        del self.client