from django.utils import timezone
from django.db import models
from app_user.models import CustomUser

class Label(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)  # Optional field
    notes = models.TextField(null=True, blank=True)  # Optional field

    def __str__(self):
        return self.title  # 'name' yerine 'title' kullanılmalı


class TimerBlock(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    label = models.ForeignKey(Label, on_delete=models.CASCADE)

    work_duration = models.IntegerField(help_text="Duration in minutes", default=0)  # Default value, no need for null
    break_duration = models.IntegerField(help_text="Duration in minutes", default=0)  # Default value, no need for null
    used_duration = models.IntegerField(help_text="Duration in minutes", default=0)  # Default value, no need for null
    percentage_of_completion = models.IntegerField(default=0, help_text="Percentage of completion")  # Default value, no need for null

    is_started = models.BooleanField(default=False)  # Default value, no need for null
    is_completed = models.BooleanField(default=False)  # Default value, no need for null
    started_at = models.DateTimeField(null=True, blank=True)  # Optional field
    completed_at = models.DateTimeField(null=True, blank=True)  # Optional field

    number_of_stop = models.IntegerField(null=True, blank=True)  # Optional field
    number_of_continue = models.IntegerField(null=True, blank=True)  # Optional field

    last_used = models.DateTimeField(null=True, blank=True)  # Optional field

    note = models.TextField(null=True, blank=True)  # Optional field
    note_title = models.CharField(max_length=100, null=True, blank=True)  # Optional field
    note_description = models.TextField(null=True, blank=True)  # Optional field

    created_at = models.DateTimeField(default=timezone.now)  # No need for null
    is_active = models.BooleanField(default=True)  # Default value, no need for null
    is_archived = models.BooleanField(default=False)  # Default value, no need for null

    def __str__(self):
        return f'{self.label} - {self.work_duration} min'


class TimerSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    timer_blocks = models.TextField(null=True, blank=True)  # Optional field

    def __str__(self):
        return f'TimerSession {self.user} - Blocks: {self.timer_blocks}'  # Added user for clarity
