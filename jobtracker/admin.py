from django.contrib import admin
from .models import JobApplication, Note, Attachment, NotificationPreference

class NoteInline(admin.TabularInline):
    model = Note
    extra = 1

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('company_title', 'position_title', 'job_type', 'status', 'created_date', 'user')
    list_filter = ('job_type', 'status', 'created_date')
    search_fields = ('company_title', 'position_title', 'user__username')
    inlines = [NoteInline, AttachmentInline]

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('job_application', 'content', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('job_application__company_title', 'content')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('job_application', 'file', 'description', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('job_application__company_title', 'description')

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_notifications', 'reminder_timing', 'job_application_updates', 'interview_reminders', 'weekly_summary')
    list_filter = ('email_notifications', 'job_application_updates', 'interview_reminders', 'weekly_summary')
    search_fields = ('user__username',)
