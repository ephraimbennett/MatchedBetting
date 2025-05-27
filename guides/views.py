from django.shortcuts import render

# Create your views here.

def guides_list(request):
    return render(request, 'guides_list.html')

def guides_detail(request):
    return render(request,  'guides_detail.html')