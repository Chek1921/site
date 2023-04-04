from rest_framework import serializers
from .models import *
from .serializers import *

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = New
        fields = "__all__"

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"

    def to_representation(self, instance):
        return instance.__rate__()

class BillNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill_name
        fields = '__all__'
    
    def to_representation(self, instance):
        return instance.__str__()

class BillRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill_rate
        fields = '__all__'
    
    def to_representation(self, instance):
        return instance.__rate__()

class BillsSerializer(serializers.ModelSerializer):
    name = BillNamesSerializer()
    rate = BillRateSerializer()

    class Meta:
        model = Bill
        fields = "__all__"