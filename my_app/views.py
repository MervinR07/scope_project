from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,'home.html')
# Create your views here.
def aboutus(request):
    return render(request,'aboutus.html')