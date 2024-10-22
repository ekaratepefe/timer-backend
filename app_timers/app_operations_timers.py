from app_timers.models import TimerBlock


class TimerOperations:
    @staticmethod
    def create_block(block_data, user):
        block = TimerBlock.objects.create(
            user=user,
            label=block_data['label'],
            work_duration=block_data['work_duration'],
            break_duration=block_data['break_duration']
        )
        return block

    @staticmethod
    def get_user_blocks(user):
        return TimerBlock.objects.filter(user=user)
