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
from django.urls import path
from main import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.news, name = 'news'),
    path('all_news', views.AllNews.as_view(), name = 'all_news'),
    path('news/<int:new_id>', views.new, name = 'new'),
    path('news_del/<int:new_id>', views.new_delete, name = 'new_del'),
    path('bills/bill_del/<int:bill_id>', views.bill_delete, name = 'bill_del'),
    path('bills/', views.bills, name = 'bills'),
    path('bills/<int:user_id>', views.bill, name = 'bill'),
    path('bills/create', views.create_bill, name = 'create_bill'),
    path('bills/rate/create', views.create_bill_rate, name = 'create_rate'),
    path('bills/name/create', views.create_bill_name, name = 'create_name'),
    path('create_report/', views.create_report, name = 'create_report'),
    path('create_district/', views.create_district, name = 'create_district'),
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
    path('reports', views.Reports.as_view(), name = 'reports'),
    path('admin_reg', views.admin_reg, name = 'admin_reg'),
    path('change_bill_rate', views.change_bill_rate, name = 'change_bill_rate'),
    path('admin_reg_del/<int:user_id>', views.admin_reg_delete, name = 'admin_reg_del'),
    path('admin_reg_aprv/<int:user_id>', views.admin_reg_approve, name = 'admin_reg_aprv'),
    path('reports_history', views.ReportsHistory.as_view(), name = 'reports_history'),
    path('my_reports', views.my_reports, name = 'my_reports'),
    path('account', views.account, name='account'),
    path('account/del/<int:user_id>', views.account_del, name='account_del'),
    path('change_district', views.change_district, name = 'change_district'),
    path('change_district/del/<int:user_id>', views.change_district_del, name = 'change_district_del'),
    path('change_district/aprv/<int:user_id>', views.change_district_approve, name = 'change_district_aprv'),
]

