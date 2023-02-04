from django.shortcuts import render, redirect
from .models import Reports
from .forms import ReportForm

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
    return render(request, 'main/success.html')

def login(request):
    return render(request, 'main/login.html', {'title': 'Вход в аккаунт', 'title': 'Успех'})

def registration(request):
    return render(request, 'main/registration.html', {'title': 'Регистрация'})