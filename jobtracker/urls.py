from django.urls import path, include
from rest_framework.routers import DefaultRouter

from jobtracker.serializers import CustomTokenObtainPairView
from .views import JobApplicationViewSet, NoteViewSet, AttachmentViewSet, NotificationPreferenceViewSet, RegisterView, UserProfileView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'jobapplications', JobApplicationViewSet, basename='jobapplication')
router.register(r'notes', NoteViewSet, basename='note')
router.register(r'attachments', AttachmentViewSet, basename='attachment')
router.register(r'notificationpreferences', NotificationPreferenceViewSet, basename='notificationpreference')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
