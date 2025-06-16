from django import forms
from .models import Settings, State
import pytz

class SettingsForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="Choose a State")
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in pytz.common_timezones])

    class Meta:
        model = Settings
        fields = ['state', 'timezone']