from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import SignUpForm, TaskForm
from .models import Task


def signup(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    form = SignUpForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "အကောင့်ဖွင့်ပြီးပါပြီ။")
        return redirect("task_list")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)
    status = request.GET.get("status", "")
    priority = request.GET.get("priority", "")
    query = request.GET.get("q", "").strip()

    if status in Task.Status.values:
        tasks = tasks.filter(status=status)
    else:
        status = ""
    if priority in Task.Priority.values:
        tasks = tasks.filter(priority=priority)
    else:
        priority = ""
    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(details__icontains=query))

    today = timezone.localdate()
    owned = Task.objects.filter(owner=request.user)
    stats = {
        "total": owned.count(),
        "open": owned.exclude(status=Task.Status.DONE).count(),
        "done": owned.filter(status=Task.Status.DONE).count(),
        "overdue": owned.exclude(status=Task.Status.DONE)
        .filter(due_date__lt=today)
        .count(),
    }
    page = Paginator(tasks, 8).get_page(request.GET.get("page"))
    return render(
        request,
        "tasks/task_list.html",
        {
            "page": page,
            "stats": stats,
            "status": status,
            "priority": priority,
            "query": query,
            "today": today,
            "status_choices": Task.Status.choices,
            "priority_choices": Task.Priority.choices,
        },
    )


@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.owner = request.user
        task.save()
        messages.success(request, "အလုပ်အသစ် ထည့်ပြီးပါပြီ။")
        return redirect("task_list")
    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "heading": "အလုပ်အသစ်"},
    )


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "ပြင်ဆင်ပြီးပါပြီ။")
        return redirect("task_list")
    return render(
        request,
        "tasks/task_form.html",
        {"form": form, "heading": "အလုပ်ပြင်ရန်", "task": task},
    )


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "ဖျက်ပြီးပါပြီ။")
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.status = (
        Task.Status.TODO if task.status == Task.Status.DONE else Task.Status.DONE
    )
    task.save(update_fields=["status", "updated_at"])
    return _redirect_back(request)


def _redirect_back(request):
    referer = request.META.get("HTTP_REFERER", "")
    parsed = urlparse(referer)
    if parsed.scheme in {"http", "https"} and parsed.netloc == request.get_host():
        return redirect(referer)
    return redirect("task_list")
