from app_timers.models import TimerSession


class StatisticsOperations:
    @staticmethod
    def calculate_user_statistics(user):
        sessions = TimerSession.objects.filter(timer_block__user=user)
        total_work_time = sum([session.work_duration for session in sessions])
        total_break_time = sum([session.break_duration for session in sessions])
        return {
            'total_work_time': total_work_time,
            'total_break_time': total_break_time
        }
