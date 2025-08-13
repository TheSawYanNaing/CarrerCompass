from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse 
from django.core.mail import send_mail
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Importing model
from .models import User 

# Importing forms
from .forms import RegisterForm, LoginForm, VerifyForm

# Importing non djanto related moduel
from random import randint
from datetime import datetime, timedelta
from validate_email import validate_email

# Create your views here.
def register(request):
    
    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("job:index"))
    
    # if get method show template 
    if request.method == "GET":
        return render(request, "authentication/register.html", {
            "register_form" : RegisterForm(),
            "login_form" : LoginForm()
        })
    
    # else handle 
    # for post method
    # creating a form
    register_form = RegisterForm(request.POST)
    
    if register_form.is_valid():
        
        data = register_form.cleaned_data 
        
        # Getting user input 
        username = data.get("username")
        email = data.get("email")
        user_type = data.get("user_type")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        
        # getting user with email
        user = User.objects.filter(email=email).first()
        
        if user:
            # error raise
            return render(request, "authentication/register.html", {
                "register_form" : register_form,
                "login_form" : LoginForm(),
                "message" : "Email already exists"
            }) 
        
        # Getting randome verificatiion code 
        verify_code = randint(100000, 999999)
        
        # Store in session
        request.session["verify_code"] = verify_code 
        request.session["user_info"] = {
            "username" : username,
            "email" : email,
            "user_type" : user_type,
            "password" : password,
            "confirm_password" : confirm_password
        }
        
        # send email
        send_mail(subject="Verification Code for CarrerCompass", message=f"{verify_code}", from_email="thesawyannaing@gmail.com", recipient_list=[email], fail_silently=False)
        
        return HttpResponseRedirect(reverse("authentication:verify"))
        
        
    # if register_form is invalid
    return render(request, "authentication/register.html", {
        "register_form" : register_form,
        "login_form" : LoginForm(),
    })
    
# For Verification during registering
def verify(request):
    
    # Check request is already authenticated
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("job:index"))
    
    else:
        
        # If get method show template
        if request.method == "GET":
            return render(request, "authentication/verify.html", {
                "form" : VerifyForm()
            })
        
        # for post method
        else:
            now = datetime.now()

            # Calculate the number of times user try to verify
            request.session["count"] = request.session.get("count", 0) + 1
            
            # if more than 5 times stop letting it
            if (request.session["count"] > 5):
                if (now - datetime.fromisoformat(request.session["last_attempt"]) > timedelta(minutes=60)):
                    request.session["count"] = 1 
                else:
                    return render(request, "authentication/verify.html", {
                        "form" : VerifyForm(),
                        "message" : "Too many attempt try again later"
                    })
                
            # Storing the time that user last attempt to verify
            request.session["last_attempt"] = now.isoformat()
                
            form = VerifyForm(request.POST)
            
            if form.is_valid():
                data = form.cleaned_data 
                
                # Getting userinput verification code
                verify_code = data.get("digit")
                
                # Check same digit or 
                if verify_code == request.session["verify_code"]:
                    
                    # Create a user 
                    user = User.objects.create_user(username=request.session["user_info"]["username"], email=request.session["user_info"]["email"], password=request.session["user_info"]["password"], user_type=request.session["user_info"]["user_type"])
                    user.save()
                    
                    # Clearing the session
                    del request.session["user_info"]
                    del request.session["verify_code"]
                    del request.session["count"]
                    del request.session["last_attempt"]
                    
                    # Logging in user
                    login(request, user)
                    return HttpResponseRedirect(reverse("job:index"))

                # if not the same
                else:
                    
                    # Adding error
                    form.add_error("digit", "Incorrect Code")
                    return render(request, "authentication/verify.html", {
                        "form" : form
                    })
            # if invalid form
            else:
                return render(request, "authentication/verify.html", {
                    "form" : form
                })
                
# For Loggin out
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("job:index"))

# For Loggin in
def login_view(request):
    
    # Check user is already login in
    if request.user.is_authenticated or request.method != "POST":
        return HttpResponseRedirect(reverse("job:index"))
    
    
    # for post method
    now = datetime.now()
    
    # Count the number of times user try to log in
    request.session["login_count"] = request.session.get("login_count", 0) + 1 
    
    # check it is more than 5
    if (request.session["login_count"] > 5):
        
        if (now - datetime.fromisoformat(request.session["login_last_attempt"]) > timedelta(minutes=60)):
            
            # Reset login count to 1
            request.session["login_count"] = 1 
        
        else:
            return render(request, "authentication/register.html", {
                "register_form" : RegisterForm(),
                "login_form" : LoginForm(),
                "is_login" : "isLogging",
                "login_message" : "Too many attempts"
            })
        
    
    # Storing the last time user try to login
    request.session["login_last_attempt"] = now.isoformat()
    
    form = LoginForm(request.POST)
    
    if form.is_valid():
        
        # Getting user input
        data = form.cleaned_data
        email = data.get("email")
        password = data.get("password")
        
        # Authentication
        user = authenticate(request, username=email, password=password)
        
        if user:
            
            del request.session["login_count"]
            del request.session["login_last_attempt"]
            login(request, user)
            return HttpResponseRedirect(reverse("job:index"))
        
        # if not authenticated
        return render(request, "authentication/register.html", {
            "register_form" : RegisterForm(),
            "login_form" : form,
            "login_message" : "Invalid Email or password",
            "is_login" : "isLogging"
        })
    
    # If invalid form 
    return render(request, "authentication/register.html", {
        "register_form" : RegisterForm(),
        "login_form" : form,
        "is_login" : "isLogging"
    })
    
# For Forgotting password
def forgot(request):
    
    # Check if user is already authenticated
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("job:index"))
    
    # for get method
    if request.method == "POST":
        
        # getting user input data
        email = request.POST.get("email")
        
        if not email or not validate_email(email):
            return render(request, "authentication/forgot.html", {
                "message" : "Invalid Email"
            })
        
        # if email exists and valid check account related to that email exists
        user = User.objects.filter(email=email).first()
        
        if not user:
            return render(request, "authentication/forgot.html", {
                "message" : "account with this email doesn't exists"
            })
        
        # if user exists generate random number and send email
        confirm_code = randint(100000, 999999)
        
        # store in session
        request.session["confirm_code"] = confirm_code 
        request.session["email"] = email 
        
        send_mail(subject="OTP code for CarrerCompass", message=f"{confirm_code}", from_email="thesawyannaing@gmail.com", recipient_list=[email], fail_silently=False)
        
        return HttpResponseRedirect(reverse("authentication:confirm"))
    
    # for post method
    else:
        return render(request, "authentication/forgot.html")
    

# For Confirmming during loggin
def confirm(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("job:index"))
    
    # for post method
    if request.method == "POST":
        
        now = datetime.now()
        
        # Counting the number of time use try to login in
        request.session["confirm_count"] = request.session.get("confirm_count", 0) + 1 
        
        # if user try over 5 times stop them
        if (request.session["confirm_count"] > 5):
            
            # if it is over 1 hour that user last attempt 
            if (now - datetime.fromisoformat(request.session["confirm_attempt"]) > timedelta(minutes=60)):
                
                # Reset confirm count to 1
                request.session["confirm_count"] = 1 
            else:
                return render(request, "authentication/confirm.html", {
                    "message" : "Too many attempt"
                })
        
        # Saving the time user attempt
        request.session["confirm_attempt"] = now.isoformat()
        # Getting user input otp
        otp = request.POST.get("otp")

        if otp == str(request.session["confirm_code"]):
            
            user = User.objects.get(email=request.session["email"])
            
            # delete session
            del request.session["confirm_code"]
            del request.session["email"]
            # loggin in user
            login(request, user)
            return HttpResponseRedirect(reverse("job:index"))
        
        return render(request, "authentication/confirm.html", {
            "message" : "Unmatch OTP Code"
        })
    
    return render(request, "authentication/confirm.html")