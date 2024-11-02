from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task
from .forms import TaskForm, TaskFilterForm
from .mixins import UserIsOwnerMixin

class TaskListView(ListView):
    model = Task
    template_name = 'tracking_app/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        priority = self.request.GET.get('priority')

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_form'] = TaskFilterForm(self.request.GET)
        return context

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tracking_app/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tracking_app/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tracking_app/task_form.html'
    success_url = reverse_lazy('task-list')

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    template_name = 'tracking_app/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
