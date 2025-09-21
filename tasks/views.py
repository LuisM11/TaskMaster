from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task, List, Category

from .models import Task


class OwnerQuerysetMixin(LoginRequiredMixin):
    """Restringe consultas al usuario autenticado."""
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class TaskListView(OwnerQuerysetMixin, ListView):
    model = Task
    template_name = "tasks/list.html"
    context_object_name = "tasks"
    paginate_by = 10  # opcional

    def get_queryset(self):
        qs = super().get_queryset().select_related("list").prefetch_related("categories")
        # Filtros simples por query params (?status=..., ?priority=..., ?list=..., ?category=...)
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        priority = self.request.GET.get("priority")
        if priority:
            qs = qs.filter(priority=priority)
        list_id = self.request.GET.get("list")
        if list_id:
            qs = qs.filter(list_id=list_id)
        category_id = self.request.GET.get("category")
        if category_id:
            qs = qs.filter(categories__id=category_id)
        return qs


class TaskDetailView(OwnerQuerysetMixin, DetailView):
    model = Task
    template_name = "tasks/detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ["title", "description", "list", "status", "priority", "due_date", "reminder_at", "categories"]
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Tarea creada correctamente.")
        return super().form_valid(form)


class TaskUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Task
    fields = ["title", "description", "list", "status", "priority", "due_date", "reminder_at", "categories"]
    template_name = "tasks/form.html"
    success_url = reverse_lazy("tasks:list")

    def form_valid(self, form):
        messages.success(self.request, "Tarea actualizada.")
        return super().form_valid(form)


class TaskDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Task
    template_name = "tasks/confirm_delete.html"
    success_url = reverse_lazy("tasks:list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tarea eliminada.")
        return super().delete(request, *args, **kwargs)


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.mark_completed()
    messages.success(request, "¡Tarea marcada como completada!")
    # Redirige a donde venga o a la lista
    return redirect(request.GET.get("next") or "tasks:list")

# ---- Lists ----
class ListOwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        return List.objects.filter(owner=self.request.user)

class ListListView(ListOwnerMixin, ListView):
    model = List
    template_name = "lists/list.html"
    context_object_name = "lists"
    ordering = ["name"]

class ListDetailView(ListOwnerMixin, DetailView):
    model = List
    template_name = "lists/detail.html"
    context_object_name = "list_obj"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Tareas de esta lista (solo del owner)
        ctx["tasks"] = Task.objects.filter(owner=self.request.user, list=self.object)\
                                   .select_related("list").prefetch_related("categories")
        return ctx

class ListCreateView(LoginRequiredMixin, CreateView):
    model = List
    fields = ["name", "description", "is_default"]
    template_name = "lists/form.html"
    success_url = reverse_lazy("tasks:lists")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ListUpdateView(ListOwnerMixin, UpdateView):
    model = List
    fields = ["name", "description", "is_default"]
    template_name = "lists/form.html"
    success_url = reverse_lazy("tasks:lists")

class ListDeleteView(ListOwnerMixin, DeleteView):
    model = List
    template_name = "lists/confirm_delete.html"
    success_url = reverse_lazy("tasks:lists")


# ---- Categories ----
class CategoryOwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

class CategoryListView(CategoryOwnerMixin, ListView):
    model = Category
    template_name = "categories/list.html"
    context_object_name = "categories"
    ordering = ["name"]

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ["name", "slug"]
    template_name = "categories/form.html"
    success_url = reverse_lazy("tasks:categories")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CategoryUpdateView(CategoryOwnerMixin, UpdateView):
    model = Category
    fields = ["name", "slug"]
    template_name = "categories/form.html"
    success_url = reverse_lazy("tasks:categories")

class CategoryDeleteView(CategoryOwnerMixin, DeleteView):
    model = Category
    template_name = "categories/confirm_delete.html"
    success_url = reverse_lazy("tasks:categories")


from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

@login_required
def logout_view(request):
    """Cierra sesión y redirige a la página de login (o a donde definas)."""
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("login")  # o usa un nombre/URL que prefieras, p. ej. "tasks:list"

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # iniciar sesión automáticamente
            messages.success(request, "Cuenta creada. ¡Bienvenido/a!")
            return redirect("tasks:list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
