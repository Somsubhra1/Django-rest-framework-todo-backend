from django.urls import path
from .views import LogoutView, RegisterView, LoginView, UserView

urlpatterns = [
    path("", UserView, name="profile"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView, name="logout"),
]
