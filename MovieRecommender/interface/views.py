from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, 'index.html')

def suggested_movies(request):
    if request.method == 'POST':
        print(request.POST.get('movies'))
    return render(request, 'final.html')