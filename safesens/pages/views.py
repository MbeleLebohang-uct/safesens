from django.shortcuts import render

def home_view(request):
    return render(request, 'pages/index.html')

def documentation_view(request):
    return render(request, 'pages/documentation.html')
