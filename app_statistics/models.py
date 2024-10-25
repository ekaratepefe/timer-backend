from django.db import models
from app_timers.models import TimerSession

class Statistics(models.Model):
    session = models.ForeignKey(TimerSession, on_delete=models.CASCADE)
    total_work_time = models.IntegerField()
    total_break_time = models.IntegerField()
    session_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Statistics for {self.session.timer_block.label} on {self.session_date}'
