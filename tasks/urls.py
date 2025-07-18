from django.urls import path
from tasks.views import Greetings, NewGreetings, dashboard, delete_task, manager_dashboard, Pr, task_details, update_task,employee_dashboard, create_task, view_task

urlpatterns = [
    path("manager_dashboard/", manager_dashboard, name="manager_dashboard"),
    path("employee_dashboard/", employee_dashboard, name="user_dashboard"),
    path("create_task/", create_task, name="create_task"),
    path("view_task/", view_task),
    path("task/<int:task_id>/details/", task_details, name='task_details'),
    path("update_task/<int:id>/", update_task, name="update_task"),
    path("delete_task/<int:id>/", delete_task, name="delete_task"),
    path('dashboard/', dashboard, name='dashboard'), 
    # path('greetings/', Greetings.as_view(), name='greetings'),
    path('greetings/', NewGreetings.as_view(greetings='hi, good day!'), name='greetings'),
    path('practice/', Pr.as_view(), name='practice')
]
