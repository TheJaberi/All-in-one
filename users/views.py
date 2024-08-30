from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, hashers
from django.contrib import messages
from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User  

def Customer_signup_view(request):
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomerSignUpForm()
    return render(request, 'users/register_customer.html', {'form': form})

def Company_signup_view(request):
    if request.method == 'POST':
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CompanySignUpForm()
    return render(request, 'users/register_company.html', {'form': form})

def Login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # email = "lammah"
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                try:
                    user = User.objects.get(email=email)
                    if not hashers.check_password(password, user.password):
                        user = None
                except User.DoesNotExist:
                    user = None
                
                if user is not None:
                    login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'Invalid email or password.')
                
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def register(request):
    return render(request, 'users/register.html')