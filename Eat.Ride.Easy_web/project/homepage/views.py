from django.shortcuts import render

# Create your views here.

def home(request):
    imgs = [{"0":1, "1":2, "2":3, "3":4},
            {"0":5, "1":6, "2":7, "3":8},
            {"0":9, "1":10, "2":11, "3":12},
            {"0":13, "1":14, "2":15, "3":16}]   
    return render(request, 'homepage/index.html',{'imgs':imgs})
