from django import forms
from .models import Settings, State

class SettingsForm(forms.ModelForm):
    state = forms.ModelChoiceField(queryset=State.objects.all(), empty_label="Choose a State")
    timezone = forms.TextInput()

    class Meta:
        model = Settings
        fields = ['state', 'timezone']