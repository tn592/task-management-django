from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.db.models.aggregates import Count
from django.shortcuts import redirect, render
from django.http import HttpResponse
from tasks.forms import TaskDetailModelForm, TaskForm, TaskModelForm
from tasks.models import Project, Task, TaskDetail
from datetime import date
from django.db.models import Q
from users.views import is_admin
from django.http import HttpResponse
from django.views import View


# Class-based re-use example
class Greetings(View):
    greetings = 'Hi Everyone'

    def get(self, request):
        return HttpResponse(self.greetings)

class NewGreetings(Greetings):
    greetings = 'Good Morning!'

    def get(self, request):
        return HttpResponse(self.greetings)

class Pr(View):
    r = 'Example Words'

    def get(self, request):
        return HttpResponse(self.r)

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Manager').exists()

# @user_passes_test(is_admin_or_manager, login_url='no_permission')
@user_passes_test(is_manager, login_url='no_permission')
def manager_dashboard(request):
    type= request.GET.get('type', 'all')
    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id',filter=Q(status='COMPLETED')),
        in_progress=Count('id',filter=Q(status='IN_PROGRESS')),
        pending=Count('id',filter=Q(status='PENDING'))
        )
    # Retriving task data
    if type=='completed':
        tasks = base_query.filter(status="COMPLETED")
    elif type=='in_progress':
        tasks = base_query.filter(status="IN_PROGRESS")
    elif type=='pending':
        tasks = base_query.filter(status="PENDING")
    else:
        tasks = base_query.all()

    context = {
        "tasks": tasks,
        "counts":counts
    }
    return render(request, "dashboard/manager-dashboard.html", context)

@user_passes_test(is_employee, login_url='no_permission')
def employee_dashboard(request):
    return render(request, "dashboard/user-dashboard.html")


@login_required 
@permission_required('tasks.add_task', login_url='no_permission')
def create_task(request):
    task_form = TaskModelForm() 
    task_detail_form = TaskDetailModelForm()
    if request.method == "POST":
        task_form = TaskModelForm(request.POST)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Created Successfully")
            return redirect(
                'create_task'
            )

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)

@login_required 
@permission_required('tasks.change_task', login_url='no_permission')
def update_task(request, id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) 
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)
    
    if request.method == "POST":
        task_form = TaskModelForm(request.POST, instance=task)
        task_detail_form = TaskDetailModelForm(request.POST, request.FILES, instance=task.details,)
        if task_form.is_valid() and task_detail_form.is_valid():
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            messages.success(request, "Task Updated Successfully")
            return redirect(
                'update_task', id
            )

    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html", context)

@login_required 
@permission_required('tasks.delete_task', login_url='no_permission')
def delete_task(request, id): 
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect(manager_dashboard)
    else:
        messages.error(request, "something went wrong")
        return redirect(manager_dashboard)

@login_required 
@permission_required('tasks.view_task', login_url='no_permission')
def view_task(request):
    projects = Project.objects.annotate(num_task=Count('task')).order_by('num_task')
    return render(
        request,
        "show_task.html",
        {"projects": projects}
    )

@login_required 
@permission_required('tasks.view_task', login_url='no_permission')
def task_details(request, task_id):
    task = Task.objects.get(id=task_id)
    status_choices = Task.STATUS_CHOICES

    if request.method == "POST":
        selected_status = request.POST.get('task_status')
        print(selected_status)
        task.status = selected_status
        task.save()
        return redirect('task_details', task.id)
    return render(request, 'task_details.html', {'task':task, 'status_choices': status_choices})


@login_required 
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_employee(request.user):
        return redirect('user_dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')

    return redirect('no_permission')


