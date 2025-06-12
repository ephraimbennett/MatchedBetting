from django.shortcuts import render, get_object_or_404
from .models import Guide

# Create your views here.

def guides_list(request):
    return render(request, 'guides_list.html')

def guides_detail(request, slug):
    article = get_object_or_404(Guide, slug=slug)
    tutorials = Guide.objects.all()
    return render(request, 'guides_detail.html', {
        'guide': article,
        'prev': '/guides',
        'next': '/guides',
        'tutorials': tutorials
    })