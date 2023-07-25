from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import Project3Config
from .views import CourseViewSet, LessonDeleteApiView, LessonListApiView, LessonRetrieveApiView, LessonCreateApiView, LessonUpdateApiView, PaymentListApiView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

app_name = Project3Config.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('course/', include(router.urls)),
    path('lessons/create/', LessonCreateApiView.as_view(), name='lesson-create'),
    path('lessons/', LessonListApiView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson-detail'),
    path('lessons/update/<int:pk>/', LessonUpdateApiView.as_view(), name='lesson-update'),
    path('lessons/delete/<int:pk>/', LessonDeleteApiView.as_view(), name='lesson-delete'),
    path('payments/', PaymentListApiView.as_view(), name='payments')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)