from django.urls import path
from tasks.views import delete_task, manager_dashboard, update_task,user_dashboard, create_task, view_task

urlpatterns = [
    path("manager_dashboard/", manager_dashboard, name="manager_dashboard"),
    path("user_dashboard/", user_dashboard),
    path("create_task/", create_task, name="create_task"),
    path("view_task/", view_task),
    path("update_task/<int:id>/", update_task, name="update_task"),
    path("delete_task/<int:id>/", delete_task, name="delete_task"),
]
