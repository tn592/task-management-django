from django.shortcuts import render
from django.http import HttpResponse

from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task


def manager_dashboard(request):
    return render(request, "dashboard/manager-dashboard.html")


def user_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


def test(request):
    names = ["Kyo", "Ishikaowa", "Loid", "Satoru"]
    count = 0
    for n in names:
        count += 1
    context = {"name": names, "age": 23, "count": count}
    return render(request, "test.html", context)


def create_task(request):
    employees = Employee.objects.all()
    form = TaskModelForm()  # For GET

    if request.method == "POST":
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For Model Form Data"""
            print(form)
            form.save()
            return render(
                request,
                "task_form.html",
                {"form": form, "message": "task added successfully"},
            )
            """For Django Form Data"""
            # data = form.cleaned_data
            # title = data.get("title")
            # description = data.get("description")
            # due_date = data.get("due_date")
            # assigned_to = data.get("assigned_to")  # list [1,2,3]

            # task = Task.objects.create(
            #     title=title, description=description, due_date=due_date
            # )
            # # Assign employee to tasks
            # for emp_id in assigned_to:
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task added successfully")

    context = {"form": form}
    return render(request, "task_form.html", context)


def view_task(request):
    # retrive all date from tasks model
    tasks = Task.objects.all()
    # retrive a specific task
    task_3 = Task.objects.get(pk=1)
    # fetch the first task
    first_task = Task.objects.first()
    return render(
        request,
        "show_task.html",
        {"tasks": tasks, "task_3": task_3, "first_task": first_task}
    )
