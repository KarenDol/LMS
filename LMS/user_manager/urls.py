"""LMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login_user, name='login_user'),
    path('register_student/', views.register_student, name='register_student'),
    path('register_parent/<IIN>/', views.register_parent, name='register_parent'),
    path('register_contract/<IIN>/', views.register_contract, name='register_contract'),
    path("logout/", views.logout_user, name='logout'),
    path('delete_student/<int:pk>/', views.delete_student, name='delete_student'),
    # path('reset_password/<int:pk>', views.reset_password, name='reset_password'),
    path('student/<IIN>/', views.student, name='student'),
    path('sign_doc/<IIN>/', views.sign_doc, name='sign_doc'),
    path('success2/', views.success2, name='success2'),
    path('qate/', views.qate, name='qate'),
    path('finance/', views.finance, name='finance'),
    path('cash/<int:entr_id>/', views.cash, name='cash'),
]
