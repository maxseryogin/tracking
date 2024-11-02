from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'deadline', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'Все')] + Task.status_choices,
        required=False,
        label='Статус',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=[('', 'Все')] + Task.priority_choices,
        required=False,
        label='Приоритет',
        widget=forms.Select(attrs={'class': 'form-control'})
    )