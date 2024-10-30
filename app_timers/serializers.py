from rest_framework import serializers
from .models import Label, TimerBlock, TimerSession, CustomUser

# Serializer for listing labels
class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'title', 'description']

# Serializer for creating a label
class LabelCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['title', 'description']

# Serializer for label detail view (without modifying the note)
class LabelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'title', 'description']

# Serializer for managing label notes
class LabelNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['notes']

# Serializer for listing work blocks
class WorkBlockListSerializer(serializers.ModelSerializer):
    label = serializers.StringRelatedField()

    class Meta:
        model = TimerBlock
        fields = ['id', 'label', 'work_duration', 'break_duration', 'percentage_of_completion']

# Serializer for listing filtered work blocks (no repetition)
class FilteredWorkBlockSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = TimerBlock  # Model adınızı güncelleyin
        fields = ['label', 'work_duration', 'break_duration']

    def get_label(self, obj):
        return {
            "id": obj.label.id,
            "title": obj.label.title
        }

# Serializer for creating a custom user
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'description']

# Serializer for the timer session model
class TimerSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerSession
        fields = ['id', 'user', 'timer_blocks']


from rest_framework import serializers
from .models import TimerBlock, TimerSession

class CreateTimerBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerBlock
        fields = ['id', 'label', 'work_duration', 'break_duration', 'note_title', 'note_description']

class TimerBlockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerBlock
        fields = '__all__'  # Tüm alanları döndürüyoruz ama Block Notes'u hariç tutabiliriz.

class TimerBlockNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerBlock
        fields = ['note', 'note_title', 'note_description']

class AddToSessionSerializer(serializers.Serializer):
    timer_block_id = serializers.IntegerField()

class RemoveFromSessionSerializer(serializers.Serializer):
    timer_block_id = serializers.IntegerField()

class WorkBlockStatsSerializer(serializers.Serializer):
    used_duration = serializers.IntegerField()

class StartWorkBlockSerializer(serializers.Serializer):
    used_duration = serializers.IntegerField()

class PauseWorkBlockSerializer(serializers.Serializer):
    used_duration = serializers.IntegerField()

class ContinueWorkBlockSerializer(serializers.Serializer):
    used_duration = serializers.IntegerField()

class StopWorkBlockSerializer(serializers.Serializer):
    used_duration = serializers.IntegerField()

from rest_framework import serializers
from .models import TimerBlock

class TimerBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerBlock
        fields = ['id']  # Include 'id'
