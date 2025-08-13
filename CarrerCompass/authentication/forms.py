from django import forms 
import re 
from validate_email import validate_email

# Regex for username
USERNAME_REGEX = r'^(?=.{5,20}$)[A-Za-z]+[0-9]*$'
PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9])(?!.*\s).{8,20}$'


# Form for Registering 
class RegisterForm(forms.Form):
    
    # Create a form that includes(username, email, password, confirmpassword, type)
    username = forms.CharField(max_length=20, label="Username", widget=forms.TextInput(attrs={
        "placeholder" : "Eg. JohnDoe",
        "class" : "username",
        "autocomplete" : "off"
    }))
    
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        "placeholder" : "Eg. Johndoe@gmail.com",
        "class" : "email",
        "autocomplete" : "off",
        "id" : "register_email"
    }))
    
    password = forms.CharField(max_length=20, label="Password", widget=forms.PasswordInput(attrs={
        "placeholder" : "********",
        "class" : "password",
        "autocomplete" : "off",
        "id" : "register_password"
    }))
    
    confirm_password = forms.CharField(max_length=20, label="Confirm Password", widget=forms.PasswordInput(attrs={
        "placeholder" : "********",
        "class" : "confirm-password",
        "autocomplete" : "off"
    }))
    
    user_type = forms.ChoiceField(label="Type", choices=[
        ("employee", "Employee"),
        ("employer", "Employer")
    ])
    
    # clean up functions
    # for username
    def clean_username(self):
        username = self.cleaned_data["username"]
        
        if re.match(USERNAME_REGEX, username):
            return username 
        
        raise forms.ValidationError("Username must be 5–20 characters, letters only, with optional numbers only at the end.")
    
    
    # for email 
    def clean_email(self):
        email = self.cleaned_data["email"]
        
        if validate_email(email):
            return email 
        
        raise forms.ValidationError("Invalid Email")
    
    # for password
    def clean_password(self):
        password = self.cleaned_data["password"]
        
        if re.match(PASSWORD_REGEX, password):
            return password 
        
        raise forms.ValidationError("Password must contain at least one uppercase letter, contain at least one number and contain at least one special character and must be between 8 to 20 characters.")
    
    # for confirmpassword
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        
        if not password or not confirm_password or password != confirm_password:
            self.add_error("confirm_password", "Passwords must match") 
        
        return cleaned_data
    
    # for type
    def clean_user_type(self):
        user_type = self.cleaned_data["user_type"]
        
        if user_type in ["employee", "employer"]:
            return user_type 
        
        raise forms.ValidationError("Invalid Type")

# Login form
class LoginForm(forms.Form):
    
    # Create form that contains(email, password)
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        "placeholder" : "Eg. johndoe@gmail.com",
        "class" : "email",
        "autocomplete" : "off",
        "id" : "login_email"
    }))
    
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={
        "placeholder" : "********",
        "class" : "password",
        "autocomplete" : "off",
        "id" : "login_password"
    }))
    
    # Validation methods
    def clean_email(self):
        email = self.cleaned_data["email"]
        if validate_email(email):
            return email 
        
        raise forms.ValidationError("Invalid Email")
    
    def clean_password(self):
        password = self.cleaned_data["password"]
        
        if re.match(PASSWORD_REGEX, password):
            return password 
        
        raise forms.ValidationError("Password must contain at least one uppercase letter, contain at least one number and contain at least one special character and must be between 8 to 20 characters.")


# Form for verification during register
class VerifyForm(forms.Form):
    digit = forms.IntegerField(label="Verification Code", min_value=111111, max_value=999999, widget=forms.NumberInput(attrs={
        "placeholder" : "XXXXXX",
        "autocomplete" : "off"
    }))