from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from users.forms import RegisterForm
from users.forms import CustomRegistrationForm
from django.contrib import messages

# Create your views here.
def sign_up(request):
	# if request.method == 'GET':
	# 	# form = RegisterForm()
	# 	form = CustomRegistrationForm()
	if request.method == 'POST':
		# form = RegisterForm(request.POST)
		form = CustomRegistrationForm(request.POST)
		if form.is_valid():
			# print(form.cleaned_data)
			form.save()
			# username = form.cleaned_data.get('username')
			# password  =form.cleaned_data.get('password1')
			# confirm_password = form.cleaned_data.get('password2')

			# if password == confirm_password:
			# 	User.objects.create(username=username, password=password)
			# else:
			# 	print("Password are not same")
			messages.success(request, "form registered Successfully")
			return redirect(
                'sign_up'
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