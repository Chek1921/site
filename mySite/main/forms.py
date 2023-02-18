from .models import Reports, Bill, CustomUser
from django.forms import ModelForm, TextInput, Textarea, EmailField
from django.contrib.auth.forms import UserCreationForm

class ReportForm(ModelForm):
    class Meta:
        model = Reports
        fields = ["title", "text"]
        widgets = {
            "title": TextInput(attrs={'class':"form-control", 'placeholder': "Ошибка счетчика"}),
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
		fields = ("username", "email", "password1", "password2", "address", "district")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

    