from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    # Tasks
    path("", views.TaskListView.as_view(), name="list"),
    path("create/", views.TaskCreateView.as_view(), name="create"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.TaskUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="delete"),
    path("<int:pk>/complete/", views.task_complete, name="complete"),

    # Lists
    path("lists/", views.ListListView.as_view(), name="lists"),
    path("lists/create/", views.ListCreateView.as_view(), name="lists_create"),
    path("lists/<int:pk>/", views.ListDetailView.as_view(), name="lists_detail"),
    path("lists/<int:pk>/edit/", views.ListUpdateView.as_view(), name="lists_edit"),
    path("lists/<int:pk>/delete/", views.ListDeleteView.as_view(), name="lists_delete"),

    # Categories
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path("categories/create/", views.CategoryCreateView.as_view(), name="categories_create"),
    path("categories/<int:pk>/edit/", views.CategoryUpdateView.as_view(), name="categories_edit"),
    path("categories/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="categories_delete"),

    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),

]
