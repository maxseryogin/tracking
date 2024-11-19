from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Task, Comment

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'file'] 
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    error_messages = {
        'password_mismatch': _('Пароли не совпадают.'),  # Исправлено
        'username': {
            'required': _('Имя пользователя обязательно.'),
            'max_length': _('Имя пользователя не может быть длиннее 150 символов.'),
            'invalid': _('Имя пользователя может содержать только буквы, цифры и следующие символы: @/./+/-/_'),
        },
        'password1': {
            'required': _('Пароль обязателен.'),
            'too_common': _('Пароль слишком простой.'),
            'password_too_similar': _('Пароль не может быть слишком похож на вашу личную информацию.'),
            'password_entirely_numeric': _('Пароль не может быть полностью числовым.'),
            'min_length': _('Пароль должен содержать минимум 8 символов.'),
        },
        'password2': {
            'required': _('Подтверждение пароля обязательно.'),
        },
    }


