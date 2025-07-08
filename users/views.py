from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import CustomRegistrationForm
from django.contrib import messages


def sign_up(request):
	if request.method == 'POST':
		form = CustomRegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			print('user', user)
			user.set_password(form.cleaned_data.get('password'))
			print(form.cleaned_data)
			user.is_active = False
			user.save()
			messages.success(request, "A confirmation mail sent. Please check your email")
			return redirect(
                'sign_in'
            )
		else:
			print("Form is not valid")
	else:
		form = CustomRegistrationForm()

	return render(request, 'registration/register.html', {'form': form})

def sign_in(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
	return render(request, 'registration/login.html')

def sign_out(request):
	if request.method == 'POST':
		logout(request)
		return redirect('sign_in')