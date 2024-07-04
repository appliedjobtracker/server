from django.db import models
from shop.models import CustomUser as User

class JobApplication(models.Model):
    JOB_TYPES = [
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Freelance', 'Freelance'),
        ('Temporary', 'Temporary'),
        ('Volunteer', 'Volunteer'),
        ('Apprenticeship', 'Apprenticeship'),
        ('Seasonal', 'Seasonal'),
        ('Co-op', 'Co-op'),
    ]
    
    STATUS_CHOICES = [
        ('In Progress', 'In Progress'),
        ('Applied', 'Applied'),
        ('Unsuccessful', 'Unsuccessful'),
        ('Interview', 'Interview'),
        ('Under Consideration', 'Under Consideration'),
        ('Offered', 'Offered'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn'),
        ('Awaiting Response', 'Awaiting Response'),
        ('Follow-up Required', 'Follow-up Required'),
        ('Hired', 'Hired'),
        ('Closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_title = models.CharField(max_length=255)
    position_title = models.CharField(max_length=255, null=True, blank=True)
    job_link = models.URLField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Applied')
    created_date = models.DateTimeField(auto_now_add=True)
    scheduled_interview_date = models.DateTimeField(null=True, blank=True)
    interview_team = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    salary_range = models.CharField(max_length=255, null=True, blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    application_method = models.CharField(max_length=255, null=True, blank=True)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    contact_phone = models.CharField(max_length=20, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    application_source = models.CharField(max_length=255, null=True, blank=True)
    resume_used = models.CharField(max_length=255, null=True, blank=True)
    cover_letter_used = models.CharField(max_length=255, null=True, blank=True)
    additional_notes = models.TextField(null=True, blank=True)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    application_status_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.company_title

class Note(models.Model):
    job_application = models.ForeignKey(JobApplication, related_name='notes', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.job_application.company_title} at {self.created_at}"

class Attachment(models.Model):
    job_application = models.ForeignKey(JobApplication, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/')
    description = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Attachment for {self.job_application.company_title}: {self.description or self.file.name}"

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    reminder_timing = models.CharField(max_length=50, default='1 day before')
    job_application_updates = models.BooleanField(default=True)
    interview_reminders = models.BooleanField(default=True)
    weekly_summary = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification preferences for {self.user.username}"

