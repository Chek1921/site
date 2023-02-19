from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import resolve_url, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required



# Create your views here.


def news(request):
    reports = Report.objects.all
    return render(request, 'main/news.html', {'title': 'Новости', 'reports': reports})

def bills(request):
    return render(request, 'main/user/bills.html', {'title': 'Ваши счета'})

def create_report(request):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'main/user/report.html', {'title': 'Создание жалобы', 'form': form})

def success(request):
    return render(request, 'main/success.html', {'title': 'Успех'})


class CustomLoginView(LoginView):
    template_name='main/reg/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Логин'
        return context

    def get_success_url(self):
        return resolve_url('news')


def registration(request):
    form = NewUserForm()
    error = ''
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            if request.POST['district'] != '1':
                user = form.save()
                login(request, user)
                return redirect("success")
            else: 
                error = 'Выберите район'

    return render (request=request, template_name="main/reg/registration.html", context={"title":'Регистрация',"form":form, "error": error})	

def logout_l(request):
    logout(request)
    return redirect("login")

class CustomPasswordResetView(PasswordResetView):
    
    email_template_name = "main/reg/password_reset_email.txt"
    subject_template_name = "main/reg/password_reset_email_name.txt"
    template_name = "main/reg/password_reset.html"

def report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    print(report)
    context = {
        'report': report,
        'title': report.title,
        }
    
    return render(request, 'main/report.html', context=context)