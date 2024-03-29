from django.urls import path
from main import api_views as view

urlpatterns = [
    path('news', view.NewsView.as_view()),
    path('news/<int:pk>/', view.NewView.as_view()),
    path('reports/', view.ReportsView.as_view()),
    path('reports/<int:pk>/', view.ReportView.as_view()),
    path('receipts/', view.ReceiptsView.as_view()),
    path('receipts/<int:pk>/', view.ReceiptView.as_view()),
    path('districts/', view.DistrictView.as_view()),
    path('bill_names/', view.BillNamesView.as_view()),
    path('registration/', view.RegistrationView.as_view()),
    path('bills/', view.BillsView.as_view()),
    path('pay/', view.PayApi.as_view()),
    path('forgot_password/', view.ForgotPasswordApi.as_view()),
]