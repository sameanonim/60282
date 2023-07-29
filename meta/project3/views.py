from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from meta.project3.pagination import MyPagination
from .permissions import IsInModeratorGroup, IsOwnerOrReadOnly
from .models import Course, Lesson, Payment
from .serializers import CourseSerializer, LessonSerializer, MyTokenObtainPairSerializer, MyTokenRefreshSerializer, PaymentSerializer
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