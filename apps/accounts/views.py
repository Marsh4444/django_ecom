from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Account
from .forms import RegistrationForm
from django.contrib import messages , auth
from django.contrib.auth.decorators import login_required

#verification email imports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str 
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


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

            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/verify_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            # (Implementation for sending email would go here)
            # send_mail(mail_subject, message, 'from@example.com', [user.email])
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request, 'Your account has be.')
            return redirect('/accounts/login/?command=verification&email='+email) # Redirect to a page that informs the user to check their email for verification
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
            return redirect('dashboard') # Redirect to dashboard page after login
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login') # Redirect back to login page on failure   
        
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'You have logged out successfully.')

    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    return HttpResponse('Account has been activated successfully! You can now login.')

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')