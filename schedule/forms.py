from django import forms
from .models import Schedule
from .models import Schedule, Course

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['course', 'start_date', 'end_date', 'weekdays', 'start_time', 'end_time']





