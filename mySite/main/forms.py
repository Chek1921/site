from .models import Reports
from django.forms import ModelForm, TextInput, Textarea

class ReportForm(ModelForm):
    class Meta:
        model = Reports
        fields = ["title", "text"]
        widgets = {
            "title": TextInput(attrs={'class':"form-control", 'placeholder': "Ошибка счетчика"}),
            "text": Textarea(attrs={'class': 'form-control', 'rows': 12})
        }