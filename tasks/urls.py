from django.urls import path
from . import views
from .views import CustomLogin, RegisterView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLogin.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page='login'), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    path('', views.main_view, name="list"),
    path('update_task/<str:pk>/', views.update_task, name="update_task"),
    path('delete/<str:pk>/', views.delete_task, name="delete"),
]
