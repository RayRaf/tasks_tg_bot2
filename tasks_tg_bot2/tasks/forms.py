from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['text', 'reminder_time']
        widgets = {
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
