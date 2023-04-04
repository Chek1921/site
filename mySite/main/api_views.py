import datetime
import json
from rest_framework import generics
from .forms import NewUserForm, PaymentForm
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.permissions import *
from .permissions import *
from django.http import HttpResponse

class RegistrationView(generics.CreateAPIView):
    model = CustomUser

    def post(self, request):
        form_data = request.data
        if form_data['district_id'] == 1:
            return HttpResponse(json.dumps['Район некоректен'])
        form_data['district'] = District.objects.get(id = form_data['district_id'])
        form = NewUserForm(form_data)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps(['YES']))
        else:
            response = []
            errors = form.errors
            for field in errors:
                error_msgs = errors[field]
                for error_msg in error_msgs:
                    response.append(error_msg)
            return HttpResponse(json.dumps(response))

class NewsView(generics.ListAPIView):
    serializer_class = NewsSerializer
    model = New

    def get_queryset(self):
        queryset = New.objects.filter(district_id = 1)
        userId = self.request.query_params.get('username', None)
        print(userId)
        if userId is not None:
            queryset = New.objects.filter(Q(district = 1) | Q(district=CustomUser.objects.get(username = userId).district))
            print(queryset)
        return queryset
    
class NewView(generics.RetrieveAPIView):
    serializer_class = NewsSerializer
    model = New
    queryset = New.objects.all()
    
class ReportsView(generics.ListCreateAPIView):
    serializer_class = ReportsSerializer
    model = Report
    permission_classes = (IsAuthenticated, )
    user = CustomUser

    def post(self, request, *args, **kwargs):
        self.user = request.user
        data = request.data
        report = Report (
            title = data['title'],
            text = data['text'],
            district = self.user.district,
            address = self.user.address,
        )
        report.save()
        print(report)
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.queryset = Report.objects.filter(address = self.user.address)
        return super().get(request, *args, **kwargs)
    
class ReportView(generics.RetrieveAPIView):
    serializer_class = ReportsSerializer
    model = Report
    permission_classes = (IsAuthenticated, IsOwner, )
    queryset = Report.objects.all()
    
class ReceiptsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    model = Payment
    permission_classes = (IsAuthenticated, )
    user = CustomUser

    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.queryset = Payment.objects.filter(address = self.user.address)
        return super().get(request, *args, **kwargs)
    
class ReceiptView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    model = Payment
    permission_classes = (IsAuthenticated, IsOwner, )
    queryset = Payment.objects.all()

class DistrictView(generics.ListAPIView):
    serializer_class = DistrictSerializer
    model = District
    queryset = District.objects.filter(id__gt = 1)

class BillsView(generics.ListAPIView):
    serializer_class = BillsSerializer
    model = Bill
    permission_classes = (IsAuthenticated, )
    user = CustomUser

    def get(self, request, *args, **kwargs):
        self.user = request.user
        self.queryset = Bill.objects.filter(address = self.user.address)
        return super().get(request, *args, **kwargs)
    
class PayApi(generics.CreateAPIView):
    model = Payment
    permission_classes = (IsAuthenticated, IsOwner, )

    def post(self, request):
        form_data = request.data
        user = request.user
        bill = Bill.objects.get(id = form_data['id'])
        form_data = {}
        form_data['address'] = user.address
        form_data['district'] = user.district
        form_data['name'] = bill.name.name
        form_data['rate_name'] = bill.rate.name
        form_data['rate_cost'] = bill.rate.cost
        form_data['current_count'] = bill.current_count
        form_data['cost'] = bill.cost
        form = PaymentForm(form_data)
        if form.is_valid():
            form.save()
            bill.time_pay = datetime.datetime.now()
            bill.current_count = bill.last_count
            bill.cost = 0
            bill.save()
            return HttpResponse(json.dumps('YES'))
        else:
            return HttpResponse(json.dumps('ОШИБКА'))