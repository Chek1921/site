from .models import *
from django.forms import ModelForm, TextInput, Textarea, EmailField
from django.contrib.auth.forms import UserCreationForm

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ["title", "text", "district", "address"]
        widgets = {
            "title": TextInput(attrs={'class':"form-control", 'placeholder': "Ошибка счетчика"}),
            "text": Textarea(attrs={'class': 'form-control', 'rows': 12})
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
        fields = []

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