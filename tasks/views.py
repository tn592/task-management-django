from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    # Work with database
    # Transform data
    # Data pasa
    # Http response / Json Response
    return HttpResponse("Welcome to the task management system")


def contact(request):
    return HttpResponse("<h1 style='color: red'>This is contact page</h1>")


def show_task(request):
    return HttpResponse("This is our task page")
