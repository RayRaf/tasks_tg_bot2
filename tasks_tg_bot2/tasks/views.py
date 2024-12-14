# tasks/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, Task
from .forms import TaskForm

def token_task_list(request):
    token = request.GET.get('token')
    if not token:
        return render(request, 'tasks/error.html', {'error': 'Токен не передан'})
    profile = get_object_or_404(UserProfile, access_token=token)
    tasks = Task.objects.filter(user=profile.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'token': token})

def token_task_edit(request, task_id):
    token = request.GET.get('token')
    if not token:
        return render(request, 'tasks/error.html', {'error': 'Токен не передан'})
    profile = get_object_or_404(UserProfile, access_token=token)
    task = get_object_or_404(Task, pk=task_id, user=profile.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            if form.cleaned_data['reminder_time']:
                form.instance.reminder_set = True
                form.instance.reminder_sent = False
            else:
                form.instance.reminder_set = False
            form.save()
            return redirect(f'/tasks/view/?token={token}')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_edit.html', {'form': form, 'token': token, 'task': task})
