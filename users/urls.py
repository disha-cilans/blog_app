from django.contrib import admin
from django.urls import path,include
from users import views

urlpatterns = [
  path('register/', views.RegisterView.as_view()),
  path('login/',views.LoginView.as_view()),
  path('user/',views.UserView.as_view()),
  path('logout/',views.LogoutView.as_view()),
]
