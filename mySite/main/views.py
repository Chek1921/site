from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import resolve_url, get_object_or_404
from django.db.models import Q, Exists
from django.views.generic.list import ListView
import datetime

# Create your views here.

def news(request):
    pay = None
    all_news = New.objects.filter(district = 1).order_by('-time_create')[:3]
    dist_news = None
    reports = None
    if request.user.is_authenticated:
        dist_news = New.objects.filter(district = request.user.district).order_by('-time_create')[:3]
        if request.user.allows == '1':
            reports = Report.objects.filter(address = request.user.address, vision = '2').order_by('-time_create')[:3]
            bills = Bill.objects.filter(address = request.user.address)
            for bill in bills:
                if datetime.datetime.date(datetime.datetime.now()) - datetime.datetime.date(bill.time_pay) >= datetime.timedelta(days=1):
                    # Payment.objects.get(id=1).time_create         |            bill.time_pay
                    pay = 'Время оплачивать счета'
    
    return render(request, 'main/news.html', {
        'title': 'Новости', 
        'all_news': all_news,
        'dist_news': dist_news,
        'reports': reports,
        'pay': pay,
        })

def account(request):
    form = ChangeDistictForm()
    error = ''
    if request.method == "POST":
        form_data = request.POST.copy()
        form_data['user'] = request.user
        form = ChangeDistictForm(form_data)
        if form.is_valid():
            if ChangeDistict.objects.filter(user = request.user).exists():
                error = "Заявка уже была отправлена"
            elif request.POST['district'] != '1' and request.POST['district'] != str(request.user.district.id):
                form.save()
                return redirect("success")
            else: 
                error = 'Выберите район'
    return render(request, 'main/user/account.html', {'title': 'Ваш аккаунт', "form": form, "error": error})

class AllNews(ListView):
    model = New
    template_name = 'main/all_news.html'
    paginate_by = 10 
    context_object_name = 'all_news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости'
        return context
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            all_news = New.objects.filter(Q(district = 1) | Q(district = self.request.user.district)).order_by('-time_create')
        else: 
            all_news = New.objects.filter(district = 1).order_by('-time_create')
        print(all_news)
        return all_news

def bill(request, user_id):
    rows = []
    user = CustomUser.objects.get(id = user_id)
    if request.user.id == user_id:
        title = "Ваши счета"
    else:
        title = "Счета " + user.address
    bills = Bill.objects.filter(address = user.address).order_by('id')
    for el in bills:
        #Накрутка счетчика
        el.current_count = round(el.current_count + 10.03, 2)
        #-----------------
        el.cost = round((el.current_count - el.last_count) * el.rate.cost, 2)
        el.save()
    rates = Bill_rate.objects.filter(Q(district = 1) | Q(district = user.district))
    for i in range(len(bills)//3+1):
        rows.append('row')
    bills_m = []            #Алгортим для создания рядов и столбцов
    bills_t = []
    i = 0                   
    for bill in bills:
        i += 1
        if i == len(bills):
            i = 1000
        bills_t.append(bill)
        if len(bills_t) == 3 or i == 1000:
            bills_m.append(bills_t)
            bills_t = []      #Тут он заканчивается
    if request.method == "POST" and request.user.allows == '2':
        bill = Bill.objects.get(id = request.POST.get("id"))
        if request.POST.get('current_count') != '':
            bill.current_count = request.POST.get('current_count')
        bill.rate = Bill_rate.objects.get(id = request.POST.get('rate'))
        bill.save()
        return redirect('success')
    return render(request, 'main/bills/bill.html', {'title': title, 'bills': bills_m, 'u': user, 'rates': rates, 'rows': rows})

def bills(request):
    search = request.GET.get('search')
    if search:
        users = CustomUser.objects.filter(address__search = search, district = request.user.district, allows = '1').order_by('address')
    else:
        users = None
    # CustomUser.objects.filter(district = request.user.district, allows = '1').order_by('address')
    return render(request, 'main/bills/bills.html', {'title': 'Счета', 'users': users})

class BillsAll(ListView):
    model = CustomUser
    template_name = 'main/bills/bills_all.html'
    paginate_by = 10 
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Счета'
        return context
    
    def get_queryset(self):
        return CustomUser.objects.filter(district = self.request.user.district, allows = '1').order_by('address')
        
def payment(request, bill_id):
    bill = Bill.objects.get(id = bill_id)
    bill.cost = round((bill.current_count - bill.last_count) * bill.rate.cost, 2)
    bill.save()
    if request.method == 'POST' and request.user.address == bill.address:
        form_data = {}
        form_data['address'] = request.user.address
        form_data['district'] = request.user.district
        form_data['name'] = bill.name.name
        form_data['rate_name'] = bill.rate.name
        form_data['rate_cost'] = bill.rate.cost
        form_data['current_count'] = bill.current_count
        form_data['cost'] = bill.cost
        form = PaymentForm(form_data)
        if form.is_valid():
            pay = form.save()
            pay.save()
            bill.time_pay = datetime.datetime.now()
            bill.current_count = bill.last_count
            bill.cost = 0
            bill.save()
            return redirect('receipts')
    return render(request, "main/bills/payment.html", {'title': 'Оплата счета', 'bill': bill})

def create_report(request):
    form = ReportForm()
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['district'] = request.user.district
        form_data['address'] = request.user.address
        form = ReportForm(form_data, request.FILES)
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

def create_bill(request):
    form = BillForm()
    if request.method == 'POST':
        form_data = request.POST.copy()
        name = Bill_name.objects.get(id = form_data['name'])
        print(name.default_rate)
        form_data['rate'] = Bill_rate.objects.get(id = name.default_rate)
        form_data['address'] = request.user.address
        form_data['last_count'] = form_data['current_count']
        form_data['cost'] = '0'
        form_data['time_pay'] = datetime.datetime.now()
        form = BillForm(form_data)
        if form.is_valid():
            print('a')
            form.save()
            return redirect('success')
    return render(request, 'main/bills/create_bill.html', {'title': 'Создание счета', 'form': form})

def create_bill_rate(request):
    form = BillRateForm()
    rates = Bill_rate.objects.filter(district = request.user.district)
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['district'] = request.user.district
        form = BillRateForm(form_data)
        if form.is_valid():
            form.save()
            return redirect('success')
    return render(request, 'main/bills/create_rate.html', {'title': 'Создание счета', 'form': form, 'rates': rates})

def create_bill_rate_del(request, bill_id):
    if request.user.allows == '2' or request.user.allows == '3':
        bill = Bill_rate.objects.get(id = bill_id)
        bills = Bill.objects.filter(rate = bill)
        for cbill in bills:
            cbill.rate = Bill_rate.objects.get(id = cbill.name.default_rate)
            cbill.save()
        bill.delete()
        return redirect("create_rate")
    else: 
        return redirect("success")

def create_bill_name(request):
    form = BillNameForm()
    rates = Bill_rate.objects.filter(district = 1)
    names = Bill_name.objects.all()
    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data['default_rate'] = 1
        form = BillNameForm(form_data)
        if form.is_valid():
            new_bill_name = form.save()
            new_rate = Bill_rate(name = 'для ' + form_data['name'], cost = 10, district = District.objects.get(id = 1), bill_name = new_bill_name)
            new_rate.save() 
            new_bill_name.default_rate = new_rate.id
            new_bill_name.save()
            return redirect('create_bill_name')
    return render(request, 'main/admin_menu/create_bill_name.html', {'names': names, 'title': 'Создание счетчика', 'form': form})


def success(request):
    return render(request, 'main/success.html', {'title': 'Успех'})

def create_district(request):
    districts = District.objects.filter(id__gt = 1)
    form = DistrictForm()
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_district')
    return render(request, 'main/admin_menu/create_district.html', {'title': 'Добавление района счетчика', 'form': form, 'districts': districts})

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

class Reports(ListView):
    model = Report
    template_name = 'main/staff/reports.html'
    paginate_by = 10 
    context_object_name = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жалобы'
        return context
    
    def get_queryset(self):
        return Report.objects.filter(district = self.request.user.district, vision = '1')

class ReportsHistory(ListView):
    model = Report
    template_name = 'main/staff/reports_history.html'
    paginate_by = 10 
    context_object_name = 'reports'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Жалобы'
        return context
    
    def get_queryset(self):
        return Report.objects.filter(district = self.request.user.district, vision = '2')

class Receipts(ListView):
    model = Payment
    template_name = 'main/user/receipts.html'
    paginate_by = 10 
    context_object_name = 'payments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Квитанции'
        return context
    
    def get_queryset(self):
        return Payment.objects.filter(address = self.request.user.address).order_by('-time_create')
    
def receipt(request, receipt_id):
    payment = Payment.objects.get(id = receipt_id)
    return render(request, 'main/user/receipt.html', {'title': 'Мои жалобы', 'payment': payment})

def my_reports(request):
    reports = Report.objects.filter(address = request.user.address, vision = '2')
    reports_active = Report.objects.filter(address = request.user.address, vision = '1')
    return render(request, 'main/user/my_reports.html', {'title': 'Мои жалобы', 'reports': reports, 'reports_active': reports_active})

def admin_reg(request):
    users = CustomUser.objects.filter(want_staff = True)
    return render(request, 'main/admin_menu/admin_registration.html', {'title': 'Заявки', 'users': users})

def change_district(request):
    users = ChangeDistict.objects.all()
    return render(request, 'main/staff/change_district.html', {'title': 'Смена района', 'users': users})

def change_bill_rate(request):
    bill_rates = Bill_rate.objects.filter(district = 1)
    if request.method == "POST":
        bill_rate = Bill_rate.objects.get(id = request.POST.get("id"))
        bill_rate.cost = request.POST.get('cost')
        bill_rate.save()
        return redirect('change_bill_rate')
    return render(request, 'main/admin_menu/change_bill_rate.html', {'title': 'Тарифы', 'bill_rates': bill_rates})

def admin_reg_delete(request, user_id):
    if request.user.allows == '3':
        user = CustomUser.objects.get(id = user_id)
        user.want_staff = False
        user.save()
        return redirect("admin_reg")
    else: 
        return redirect("news")
    
def change_district_del(request, user_id):
    if request.user.allows == '2':
        user = ChangeDistict.objects.get(id = user_id)
        user.delete()
        return redirect("change_district")
    else: 
        return redirect("news")

def change_district_approve(request, user_id):
    if request.user.allows == '2':
        application = ChangeDistict.objects.get(id = user_id)
        user = CustomUser.objects.get(id = application.user.id)
        reports = Report.objects.filter(address = user.address)
        for el in reports:
            el.district = application.district
            el.save()
        user.district = application.district
        user.save()
        application.delete()
        return redirect("change_district")
    else: 
        return redirect("news")
    
def bill_name_delete(request, bill_id):
    if request.user.allows == '3':
        bill_name = Bill_name.objects.get(id = bill_id)
        bill_name.delete()
        return redirect("create_name")
    else: 
        return redirect("news")
    
def district_delete(request, district_id):
    if request.user.allows == '3' and district_id != 1:
        district = District.objects.get(id = district_id)
        district.delete()
        return redirect("create_district")
    else: 
        return redirect("news")
    
def new_delete(request, new_id):
    if request.user.allows == '2':
        new = New.objects.get(id = new_id)
        new.delete()
        return redirect("news")
    else: 
        return redirect("news")
    
def bill_delete(request, bill_id):
    if request.user.allows == '2':
        bill = Bill.objects.get(id = bill_id)
        bill.delete()
        return redirect("bills")
    else: 
        return redirect("success")

def admin_reg_approve(request, user_id):
    if request.user.allows == '3':
        user = CustomUser.objects.get(id = user_id)
        
        user.allows = 2
        user.want_staff = False
        user.save()
        return redirect("admin_reg")
    else: 
        return redirect("news")
    
def account_del(request, user_id):
    if request.user.id == user_id:
        user = CustomUser.objects.get(id = user_id)
        bills = Bill.objects.filter(address = user.address)
        reports = Report.objects.filter(address = user.address)
        for el in reports:
            el.address = 'УДАЛЕННЫЙ АККАУНТ'
        bills.delete()
        user.delete()
        return redirect('news')
    else:
        return redirect('news')