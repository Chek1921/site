from rest_framework import generics
from .models import *
from .serializers import *
from django.db.models import Q
from rest_framework.permissions import *
from .permissions import *

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
