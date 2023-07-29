from django.shortcuts import render
from ProductApp.models import Category
from django.http import HttpResponse, JsonResponse

def index(request):
    context = {
        "categories" : list(Category.objects.all())[:9]
    }
    return render(request, 'Homepage/index.html', context)

def all_categories(request):
    context = {
        "categories" : Category.objects.all()
    }
    return render(request, 'Homepage/all-categories.html', context)


def search_category(request, search_word):
    categories = Category.objects.values()
    filtered_categories = []
    if search_word != "_empty_":
        for category in categories:
            if category['name'].lower().find(search_word.lower()) != -1:
                filtered_categories.append(category)
    else: 
        filtered_categories = list(categories)
    return JsonResponse({'data':filtered_categories[:9]})

