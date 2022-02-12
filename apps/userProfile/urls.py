from django.urls import path
from .views import SignUpView, LoginView, MyAccountView

urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('myaccount', MyAccountView.as_view())
]