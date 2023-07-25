from rest_framework import serializers
from .models import Course, Lesson, Payment

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