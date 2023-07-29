from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from meta.project3.pagination import MyPagination
from .permissions import IsInModeratorGroup, IsOwnerOrReadOnly
from .models import Course, Lesson, Payment, Subscription
from .serializers import CourseSerializer, LessonSerializer, MyTokenObtainPairSerializer, MyTokenRefreshSerializer, PaymentSerializer, SubscriptionSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsInModeratorGroup, IsOwnerOrReadOnly]
    pagination_class = MyPagination

    def get(self, request):
        queryset = self.queryset
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = CourseSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    @api_view(['GET'])
    def course_list(request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class LessonListApiView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = MyPagination

    def get(self, request):
        queryset = self.queryset
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = LessonSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)

class LessonRetrieveApiView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsInModeratorGroup, IsOwnerOrReadOnly]
    http_method_names = ['get', 'head']

class LessonCreateApiView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

class LessonUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsInModeratorGroup]

class LessonDeleteApiView(generics.RetrieveDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

class PaymentListApiView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]
    filterset_fields = ['payment_method','course_or_lesson']
    ordering_fields = ['payment_date']

class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class UserTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

class SubscriptionCreateApiView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=400)
        
        subscription, created = Subscription.objects.get_or_create(user=user, course=course)
        subscription.subscribed = True
        subscription.save()

        return Response({'success': 'Подписка установлена'}, status=200)
    
class SubscriptionDeleteApiView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def delete(self, request, *args, **kwargs):

        user = request.user
        course_id = request.query_params.get('course_id')
        
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({'error': 'Курс не найден'}, status=400)
        
        subscription = Subscription.objects.filter(user=user, course=course, subscribed=True).first()
        if subscription:
            subscription.subscribed = False
            subscription.save()

        return Response({'success': 'Подписка удалена'}, status=200)