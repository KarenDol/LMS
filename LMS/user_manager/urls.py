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
from django.urls import path, re_path
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
    path('student_card/<IIN>/', views.student_card, name='student_card'),
    path('parent_card/<IIN>/', views.parent_card, name='parent_card'),
    path('contract_card/<IIN>/', views.contract_card, name='contract_card'),
    path('sign_doc/<IIN>/', views.sign_doc, name='sign_doc'),
    path('finance/', views.finance, name='finance'),
    path('cash/<int:entr_id>/', views.cash, name='cash'),
    path('user_settings/', views.user_settings, name='user_settings'),
    path('404/<error_code>', views.error, name='error'),

    #API urls
    path('api/user-info/', views.get_user_info, name='get_user_info'),
    re_path(r'^api/serve_static/(?P<filename>.+)$', views.serve_static, name='serve_static'),
]