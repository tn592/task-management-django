from django.contrib.auth import login, logout

# from django.contrib.auth import authenticate
from django.shortcuts import HttpResponse, redirect, render

# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import CustomRegistrationForm
from django.contrib import messages

# from django.contrib.auth.forms import AuthenticationForm
from users.forms import LoginForm
from django.contrib.auth.tokens import default_token_generator


def sign_up(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print("user", user)
            user.set_password(form.cleaned_data.get("password1"))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(
                request, "A confirmation mail sent. Please check your email"
            )
            return redirect("sign_in")
        else:
            print("Form is not valid")
    else:
        form = CustomRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


def sign_in(request):
    # form  = AuthenticationForm()
    form = LoginForm()
    if request.method == "POST":
        # form = AuthenticationForm(data=request.POST)
        form = LoginForm(data=request.POST)
        # username = request.POST.get('username')
        # password = request.POST.get('password')

        # user = authenticate(request, username=username, password=password)

        # if user is not None:
        #   login(request, user)
        #   return redirect('home')
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html", {"form": form})


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("sign_in")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign_in")
        else:
            return HttpResponse("Invalid Id or token")
    except User.DoesNotExist:
        return HttpResponse("User not Found")
