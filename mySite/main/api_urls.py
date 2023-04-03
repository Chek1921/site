from django.urls import path
from main import api_views as view

urlpatterns = [
    path('news', view.NewsView.as_view()),
    path('news/<int:pk>/', view.NewView.as_view()),
    path('reports/', view.ReportsView.as_view()),
    path('reports/<int:pk>/', view.ReportView.as_view()),
    path('receipts/', view.ReceiptsView.as_view()),
]