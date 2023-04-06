import base64
import datetime
from io import BytesIO
import json
from rest_framework import generics
from .forms import BillForm, NewUserForm, PaymentForm
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.permissions import *
from .permissions import *
from django.http import HttpResponse
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.views import APIView
from django.contrib.auth.forms import PasswordResetForm

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
        if userId is not None:
            queryset = New.objects.filter(Q(district = 1) | Q(district=CustomUser.objects.get(username = userId).district))
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
        base64_image = request.data['photo']
        image_data = base64.b64decode(base64_image)
        image_file = BytesIO(image_data)
        file_name = f'{datetime.datetime.now()}.jpg'
        file = InMemoryUploadedFile(image_file, None, file_name, 'image/jpeg', len(image_data), None)
        report = Report (
            title = data['title'],
            text = data['text'],
            district = self.user.district,
            address = self.user.address,
            photo = file,
        )
        report.save()
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

class BillNamesView(generics.ListAPIView):
    serializer_class = BillNamesSerializer
    model = Bill_name
    queryset = Bill_name.objects.all()

class BillsView(generics.ListCreateAPIView):
    serializer_class = BillsSerializer
    model = Bill
    permission_classes = (IsAuthenticated, )
    user = CustomUser

    def post(self, request):
        form_data = request.data
        user = request.user
        name = Bill_name.objects.get(id = form_data['name'])
        form_data['rate'] = Bill_rate.objects.get(id = name.default_rate)
        form_data['address'] = user.address
        form_data['last_count'] = form_data['current_count']
        form_data['cost'] = '0'
        form_data['time_pay'] = datetime.datetime.now()
        form = BillForm(form_data)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps('YES'))
        else:
            return HttpResponse(json.dumps('ОШИБКА'))

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
        
class BillCreateApi(generics.CreateAPIView):
    model = Bill
    permission_classes = (IsAuthenticated, )

class ForgotPasswordApi(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data['email']
            form = PasswordResetForm({'email': email})
            if form.is_valid():
                form.save(
                    use_https=request.is_secure(),
                    request=request,
                )
            return HttpResponse(json.dumps({"email":['На указанную почту отправлено письмо']}))