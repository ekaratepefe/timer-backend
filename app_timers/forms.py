from django import forms
from .models import TimerBlock

class TimerBlockForm(forms.ModelForm):
    class Meta:
        model = TimerBlock
        fields = ['label', 'work_duration', 'break_duration']
        widgets = {
            'label': forms.TextInput(attrs={'placeholder': 'Enter working label'}),
            'work_duration': forms.NumberInput(attrs={'placeholder': 'Work duration in minutes'}),
            'break_duration': forms.NumberInput(attrs={'placeholder': 'Break duration in minutes'}),
        }
