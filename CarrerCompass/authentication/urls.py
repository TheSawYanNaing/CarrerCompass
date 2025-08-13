from django.urls import path 
from . import views

app_name = "authentication"

urlpatterns = [
    path("/register", views.register, name="register"),
    path("/verify", views.verify, name="verify"),
    path("/logout", views.logout_view, name="logout"),
    path("/login", views.login_view, name="login"),
    path("/forgot", views.forgot, name="forgot"),
    path("/confirm", views.confirm, name="confirm")
]
