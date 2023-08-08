from django.conf import settings
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import Project3Config
from .views import CourseViewSet, LessonDeleteApiView, LessonListApiView, LessonRetrieveApiView, LessonCreateApiView, LessonUpdateApiView, PaymentListApiView, SubscriptionCreateApiView, SubscriptionDeleteApiView, UserTokenObtainPairView, UserTokenRefreshView
from django.conf.urls.static import static

app_name = Project3Config.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/create/', LessonCreateApiView.as_view(), name='lesson-create'),
    path('lessons/', LessonListApiView.as_view(), name='lesson-list'),
    path('lesson/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson-detail'),
    path('lesson/update/<int:pk>/', LessonUpdateApiView.as_view(), name='lesson-update'),
    path('lesson/delete/<int:pk>/', LessonDeleteApiView.as_view(), name='lesson-delete'),
    path('course/', include(router.urls)),
    path('payments/', PaymentListApiView.as_view(), name='payments'),
    path('token/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', UserTokenRefreshView.as_view(), name='token-refresh'),
    path('subscriptions/create/', SubscriptionCreateApiView.as_view(), name='subscription-create'),
    path('subscriptions/delete/', SubscriptionDeleteApiView.as_view(), name='subscription-delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)