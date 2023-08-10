from datetime import timedelta
from rest_framework import serializers
from .validators import EvenYoutubeValidator
from .models import Course, Lesson, Payment, Subscription
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [EvenYoutubeValidator(field='video_link')]

class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    subscription = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'preview', 'description','number_of_lessons', 'lessons']

    def get_number_of_lessons(self, course):
        return course.lesson_set.count()
    
    def get_subscription(self, course):
        subscription = Subscription.objects.filter(user=self.context['request'].user, course=course).first()
        
        if subscription:
            return {
                'user': subscription.user.username,
                'course': subscription.course.title,
                'subscribed': subscription.subscribed
            }
        else:
            return {}

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_method', 'course_or_lesson']

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        refresh.set_exp(lifetime=timedelta(days=7))
        data['refresh'] = str(refresh)
        return data

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['user', 'course', 'subscribed']