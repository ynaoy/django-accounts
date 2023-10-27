from django.urls import path
from . import views

app_name = "logins"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"), 
    path('update/<int:pk>', views.UpdateView.as_view(), name="update"), 
    path('update_password/<int:pk>', views.UpdatePasswordView.as_view(), name="update_password"), 
]