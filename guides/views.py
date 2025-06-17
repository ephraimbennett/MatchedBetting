from django.shortcuts import render, get_object_or_404
from .models import Guide
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Q
import json

# Create your views here.

def guides_list(request):
    tutorials = get_tutorial()
    tutorials_json = json.dumps([{'title': t.title, 'slug': t.slug} for t in tutorials])
    return render(request, 'guides_list.html', {
        'tutorials': tutorials,
        'tutorials_json': tutorials_json    
    })

def guides_detail(request, slug):
    article = get_object_or_404(Guide, slug=slug)
    tutorials = get_tutorial()

    prev, next = get_prev_next(slug, tutorials)

    return render(request, 'guides_detail.html', {
        'guide': article,
        'prev': prev,
        'next': next,
        'tutorials': tutorials
    })

def get_prev_next(slug, tutorials):
    prev = next = None
    i = 0
    for t in tutorials:
        if slug == t.slug:
            prev = None if i == 0 else tutorials[i - 1]
            next = None if i == len(tutorials) - 1 else tutorials[i + 1]
        i += 1
    return prev, next

def get_tutorial():
    res = []
    slugs = ['what-is-matched-betting', 'all-about-bonus-bets', 'priced-in-on-profit-boosts', 'serious-on-site-credit',
             'succeed-with-second-chance', 'identifying-sportsbook-promotions']
    for s in slugs:
        res.append(Guide.objects.get(slug=s))
    return res

@require_GET
def search(request):
    query = request.GET.get('q')

    if not query:
        return JsonResponse({'results': []})
    
    # should select the articles that match words in this query
    matched = Guide.objects.filter(Q(title__icontains=query)).values('title', 'slug')[:10]
    return JsonResponse({'results': list(matched)})
