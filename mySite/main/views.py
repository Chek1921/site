from django.shortcuts import render

# Create your views here.


def news(request):
    return render(request, 'main/news.html')

def bills(request):
    return render(request, 'main/bills.html')

def report(request):
    return render(request, 'main/report.html')