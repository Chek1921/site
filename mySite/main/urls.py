"""mySite URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.news, name = 'news'),
    path('all_news', views.all_news, name = 'all_news'),
    path('news/<int:report_id>', views.new, name = 'new'),
    path('bills/', views.bills, name = 'bills'),
    path('create_report/', views.create_report, name = 'create_report'),
    path('create_new/', views.create_new, name = 'create_new'),
    path('success', views.success, name = 'success'),
    path('login', views.CustomLoginView.as_view(), name = 'login'),
    path('registration/', views.registration, name = 'registration'),
    path('logout/', views.logout_l, name = 'logout'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='main/reg/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/reg/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/reg/password_reset_complete.html'), name='password_reset_complete'), 
    path("password_reset", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path('reports/<int:report_id>', views.report, name = 'report'),
    path('reports', views.reports, name = 'reports'),
    path('admin_reg', views.admin_reg, name = 'admin_reg'),
    path('admin_reg_del/<int:user_id>', views.admin_reg_delete, name = 'admin_reg_del'),
    path('admin_reg_aprv/<int:user_id>', views.admin_reg_approve, name = 'admin_reg_aprv'),
    path('reports_history', views.reports_history, name = 'reports_history'),
    path('my_reports', views.my_reports, name = 'my_reports'),
]

