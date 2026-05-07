from django import forms
from .models import HarvesterActivity, TeamLeader, Group

class HarvesterActivityForm(forms.ModelForm):
    class Meta:
        model = HarvesterActivity
        fields = ['group', 'team_leader', 'activity', 'start_time', 'end_time']

        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }