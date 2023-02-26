from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import resolve_url, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q



# Create your views here.


def news(request):
    all_news = New.objects.filter(district = 1).order_by('-time_create')[:3]
    dist_news = None
    reports = None
    if request.user.is_authenticated:
        dist_news = New.objects.filter(district = request.user.district).order_by('-time_create')[:3]
        if request.user.allows == '1':
            reports = Report.objects.filter(address = request.user.address, vision = '2').order_by('-time_create')[:3]
    
    return render(request, 'main/news.html', {
        'title': 'Новости', 
        'all_news': all_news,
        'dist_news': dist_news,
        'reports': reports,
        })

def all_news(request):
    if request.user.is_authenticated:
        all_news = New.objects.filter(Q(district = 1) | Q(district = request.user.district)).order_by('-time_create')
    else: 
        all_news = New.objects.filter(district = 1).order_by('-time_create')
    
    return render(request, 'main/all_news.html', {
        'title': 'Новости', 
        'all_news': all_news,
        })

def bill(request, user_id):
    user = CustomUser.objects.get(id = user_id)
    if request.user.id == user_id:
        title = "Ваши счета"
    else:
        title = "Счета " + user.address
    bills = Bill.objects.filter(address = user.address)
    for el in bills:
        el.cost = (el.current_count - el.last_count) * el.rate.cost
    rates = Bill_rate.objects.filter(Q(district = 1) | Q(district = user.district))
    return render(request, 'main/bills/bill.html', {'title': title, 'bills': bills, 'u': user, 'rates': rates})

def bills(request):
    users = CustomUser.objects.filter(district = request.user.district, allows = '1')
    return render(request, 'main/bills/bills.html', {'title': 'Счета', 'users': users})

def create_report(request):
    form = ReportForm()
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['district'] = request.user.district
        form_data['address'] = request.user.address
        form = ReportForm(form_data)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'main/user/create_report.html', {'title': 'Создание жалобы', 'form': form})

def create_new(request):
    form = NewForm()
    if request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'main/staff/create_new.html', {'title': 'Создание новости', 'form': form})

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
    context = {
        'report': report,
        'title': report.title,
        }
    if request.method == "POST":
        report.a_title = request.POST.get("a_title")
        report.a_text = request.POST.get("a_text")
        report.vision = '2'
        report.save()

    if (request.user.is_authenticated and request.user.address == report.address) or (request.user.is_authenticated and request.user.allows == '2' and request.user.district == report.district):
        return render(request, 'main/report.html', context=context)
    else:
        return redirect('news')

def new(request, new_id):
    new = get_object_or_404(New, id=new_id)
    context = {
        'new': new,
        'title': new.title,
        }
    
    return render(request, 'main/new.html', context=context)

def reports(request):
    reports_actual = Report.objects.filter(district = request.user.district, vision = '1')
    return render(request, 'main/staff/reports.html', {'title': 'Жалобы', 'reports': reports_actual})

def reports_history(request):
    reports_history = Report.objects.filter(district = request.user.district, vision = '2')
    return render(request, 'main/staff/reports_history.html', {'title': 'Жалобы', 'reports': reports_history})

def my_reports(request):
    reports = Report.objects.filter(address = request.user.address, vision = '2')
    reports_active = Report.objects.filter(address = request.user.address, vision = '1')
    return render(request, 'main/user/my_reports.html', {'title': 'Мои жалобы', 'reports': reports, 'reports_active': reports_active})

def admin_reg(request):
    users = CustomUser.objects.filter(want_staff = True)
    return render(request, 'main/admin_menu/admin_registration.html', {'title': 'Заявки', 'users': users})

def admin_reg_delete(requset, user_id):
    if requset.user.allows == '3':
        user = CustomUser.objects.get(id = user_id)
        user.want_staff = False
        return redirect("admin_reg")
    else: 
        return redirect("news")
    
def new_delete(requset, new_id):
    if requset.user.allows == '2':
        new = New.objects.get(id = new_id)
        new.delete()
        return redirect("news")
    else: 
        return redirect("news")

def admin_reg_approve(requset, user_id):
    if requset.user.allows == '3':
        user = CustomUser.objects.get(id = user_id)
        
        user.allows = 2
        user.want_staff = False
        user.save()
        return redirect("admin_reg")
    else: 
        return redirect("news")