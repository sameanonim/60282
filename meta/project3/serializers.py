from datetime import timedelta
from rest_framework import serializers
from .models import Course, Lesson, Payment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    class Meta:
        model = Course
        fields = ['title', 'preview', 'description','number_of_lessons', 'lessons']

    def get_number_of_lessons(self, course):
        return course.lesson_set.count()
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_method', 'course_or_lesson']
    
class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        token = self.get_token(self.user)
        token.set_exp(lifetime=timedelta(days=7))
        return data
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token