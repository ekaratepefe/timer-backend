# app_timers/serializers.py

from rest_framework import serializers
from .models import Label, TimerBlock

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'user', 'title', 'description', 'notes']

class TimerBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerBlock
        fields = ['id', 'user', 'label', 'work_duration', 'break_duration', 'used_duration', 'percentage_of_completion', 'note_title', 'note_description', 'note']

    def create(self, validated_data):
        # Check if a label with the given title exists, otherwise create a new one
        label_title = self.context['request'].data.get('label_title', None)
        if label_title:
            label, created = Label.objects.get_or_create(title=label_title, user=validated_data['user'])
            validated_data['label'] = label
        return super().create(validated_data)
