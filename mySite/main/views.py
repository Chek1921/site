from django.shortcuts import render, redirect
from .models import Reports, CustomUser
from .forms import ReportForm, NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import resolve_url
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required



# Create your views here.


def news(request):
    reports = Reports.objects.all
    return render(request, 'main/news.html', {'title': 'Новости', 'reports': reports})

def bills(request):
    return render(request, 'main/bills.html', {'title': 'Ваши счета'})

def report(request):
    form = ReportForm()
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'main/report.html', {'title': 'Создание жалобы', 'form': form})

def success(request):
    return render(request, 'main/success.html', {'title': 'Успех'})


class CustomLoginView(LoginView):
    template_name='main/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Логин'
        return context

    def get_success_url(self):
        return resolve_url('news')


def registration(request):
    form = NewUserForm()

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("success")

    return render (request=request, template_name="main/registration.html", context={"form":form})	

def logout_l(request):
    logout(request)
    return redirect("login")

class CustomPasswordResetView(PasswordResetView):
    
    email_template_name = "main/password_reset_email.txt"
    subject_template_name = "main/password_reset_email_name.txt"
    template_name = "main/password_reset.html"