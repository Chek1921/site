from .models import *
from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, ImageField
from django.contrib.auth.forms import UserCreationForm

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ["address", "district", 'name', 'rate_name', 'rate_cost', 'current_count', 'cost']

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["title", "text", "district", "address", "photo"]
        widgets = {
            "title": TextInput(attrs={'class':"form-control", 'placeholder': "Ошибка счетчика"}),
            "text": Textarea(attrs={'class': 'form-control', 'rows': 12}),
        }

class NewForm(ModelForm):
    class Meta:
        model = New
        fields = ["title", "text", "district"]
        widgets = {
            "title": TextInput(attrs={'class':"form-control", 'placeholder': "Первая новость"}),
            "text": Textarea(attrs={'class': 'form-control', 'rows': 12})
        }

class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = ["name", "last_count", "current_count", "address", "rate", "cost"]
        widgets = {
            "name": Select(attrs = {'class':"form-control"}),
            "current_count": NumberInput(attrs = {'class':"form-control"}),
        }

class BillRateForm(ModelForm):
    class Meta:
        model = Bill_rate
        fields = ["name", "cost", "district", "bill_name"]
        widgets = {
            "name": TextInput(attrs={'class':"form-control"}),
            "bill_name": Select(attrs = {'class':"form-control"}),
            "cost": NumberInput(attrs = {'class':"form-control"}),
        }

class BillNameForm(ModelForm):
    class Meta:
        model = Bill_name
        fields = ["name", "unit", "default_rate"]
        widgets = {
            "name": TextInput(attrs={'class':"form-control"}),
            "unit": TextInput(attrs = {'class':"form-control"}),
        }

class ChangeDistictForm(ModelForm):
    class Meta:
        model = ChangeDistict
        fields = ["user", "district"]
        widgets = {
             'district': Select(attrs={'class': "form-control"})
        }

class DistrictForm(ModelForm):
     class Meta:
          model = District
          fields = ['district']
          widgets = {
               "district": TextInput(attrs={'class':"form-control"}),
          }

# Create your forms here.

class NewUserForm(UserCreationForm):
	
	class Meta:
		model = CustomUser
		fields = ("username", "email", "password1", "password2", "address", "district", "want_staff")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user