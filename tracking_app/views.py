from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Task, Comment, Like
from .forms import CustomUserCreationForm, TaskForm, TaskFilterForm, CommentForm
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.all()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            comment_form = CommentForm(request.POST, request.FILES)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.task = self.object
                comment.save()
                return redirect('task-detail', pk=self.object.pk)
        return redirect('login')
    

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

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'tracking_app/comment_form.html'

    def form_valid(self, form):
        form.save()
        return redirect('task-detail', pk=self.object.task.pk)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.object.task.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'tracking_app/comment_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


    def get_success_url(self):
        return reverse_lazy('task-list')

@method_decorator(login_required, name='dispatch')
class LikeCommentView(View):
    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, comment=comment)
        if not created:
            like.delete()  # If the like already exists, remove it (toggle functionality)
        return redirect('task_detail', pk=comment.task.pk)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task-list') 
    else:
        form = CustomUserCreationForm()

    return render(request, 'tracking_app/register.html', {'form': form})
@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if not Like.objects.filter(user=request.user, comment=comment).exists():
        Like.objects.create(user=request.user, comment=comment)
        comment.likes += 1
        comment.save()

    return redirect('task-detail', pk=comment.task.pk)
