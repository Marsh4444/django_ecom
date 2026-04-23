from django.shortcuts import redirect, render
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name      = form.cleaned_data['first_name']
            last_name       = form.cleaned_data['last_name']
            email           = form.cleaned_data['email']
            phone_number    = form.cleaned_data['phone_number']
            password        = form.cleaned_data['password']
            username        = email.split('@')[0] # Generate username from email

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Here you would typically authenticate the user and log them in
        # For now, we will just display a success message

        # Authenticate the user
        user = auth.authenticate(request, email=email, password=password)
        # Log the user in if authentication is successful
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You have logged in successfully.')
            return redirect('home') # Redirect to home page after login
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login') # Redirect back to login page on failure   
        
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'You have logged out successfully.')

    return redirect('home')

