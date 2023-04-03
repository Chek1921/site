from rest_framework import serializers
from .models import *

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
