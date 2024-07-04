from rest_framework import viewsets, filters, status, generics, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import JobApplication, Note, Attachment, NotificationPreference
from .serializers import JobApplicationSerializer, NoteSerializer, AttachmentSerializer, NotificationPreferenceSerializer, RegisterSerializer, UserProfileSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['company_title']

    def get_queryset(self):
        return JobApplication.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def filter_by_status(self, request):
        status = request.query_params.get('status')
        if status is not None:
            applications = self.get_queryset().filter(status=status)
            serializer = self.get_serializer(applications, many=True)
            return Response(serializer.data)
        return Response({"detail": "Status parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Note.objects.filter(job_application__user=self.request.user)

    def perform_create(self, serializer):
        job_application = get_object_or_404(JobApplication, id=self.request.data.get('job_application'), user=self.request.user)
        serializer.save(job_application=job_application)

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Attachment.objects.filter(job_application__user=self.request.user)

    def perform_create(self, serializer):
        job_application = get_object_or_404(JobApplication, id=self.request.data.get('job_application'), user=self.request.user)
        serializer.save(job_application=job_application)

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return NotificationPreference.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get', 'put'], url_path='preferences')
    def user_preferences(self, request):
        user = request.user
        preferences, created = NotificationPreference.objects.get_or_create(user=user)
        if request.method == 'PUT':
            serializer = self.get_serializer(preferences, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(preferences)
        return Response(serializer.data)