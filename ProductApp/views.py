from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from Account.models import CustomUser
from .models import Category, Product, Review
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
import json
from .forms import AddProductForm

def comments(request, slug):
    current_product = Product.objects.get(slug=slug)
    review_per_page = 10
    context = {
        "categories" : list(Category.objects.all())[:9],
        "slug" : slug,
        "current_product" : current_product,
        "product_reviews" : Review.objects.filter(product__slug = slug, is_active = True),
        "seller_reviews" : Review.objects.filter(to_user__slug = current_product.user.slug, is_active = True),
    }

    product_reviews_length = Review.objects.filter(product__slug = slug, is_active = True).count()
    seller_reviews_length = Review.objects.filter(to_user__slug = current_product.user.slug, is_active = True).count()

    if product_reviews_length / review_per_page > 1:
        product_all_reviews_link = True
    else: 
        product_all_reviews_link = False

    if seller_reviews_length / review_per_page > 1:
        seller_all_reviews_link = True
    else: 
        seller_all_reviews_link = False

    context.update({
        'product_reviews_length' : product_reviews_length,
        'seller_reviews_length' : seller_reviews_length,
        'product_all_reviews_link' : product_all_reviews_link,
        'seller_all_reviews_link' : seller_all_reviews_link
    })

    if 'product-comments' in request.build_absolute_uri():
        _product_reviews = context['product_reviews']
        paginator = Paginator(_product_reviews, review_per_page)
        page_number = request.GET.get('page')
        _product_reviews = paginator.get_page(page_number)
        context.update({
            'reviews' : _product_reviews,
        })

    elif 'seller-comments' in request.build_absolute_uri():
        _seller_reviews = Review.objects.filter(to_user__slug = current_product.user.slug, is_active = True),
        paginator = Paginator(_seller_reviews, review_per_page)
        page_number = request.GET.get('page')
        _seller_reviews = paginator.get_page(page_number)
        context.update({
            'reviews' : _seller_reviews,
        })

    return render(request, "ProductApp/product_comments.html", context)

def productDetail(request, slug):
    current_product = Product.objects.get(slug=slug)
    review_per_page = 7
    context = {
        "categories" : list(Category.objects.all())[:9],
        "slug" : slug,
        "current_product" : current_product,
        "product_reviews" : list(Review.objects.filter(product__slug = slug, is_active = True))[:review_per_page],
        "seller_reviews" : list(Review.objects.filter(to_user__slug = current_product.user.slug, is_active = True))[:review_per_page],
    } 

    product_reviews_length = Review.objects.filter(product__slug = slug, is_active = True).count()
    seller_reviews_length = Review.objects.filter(to_user__slug = current_product.user.slug, is_active = True).count()

    if product_reviews_length / review_per_page > 1:
        product_all_reviews_link = True
    else: 
        product_all_reviews_link = False

    if seller_reviews_length / review_per_page > 1:
        seller_all_reviews_link = True
    else: 
        seller_all_reviews_link = False

    context.update({
        'product_reviews_length' : product_reviews_length,
        'seller_reviews_length' : seller_reviews_length,
        'product_all_reviews_link' : product_all_reviews_link,
        'seller_all_reviews_link' : seller_all_reviews_link
    })

    if Product.objects.filter(Q(fav_user__username = request.user.username) & Q(slug=slug)).exists():
        print('girdi')
        context.update({
            'favorite' : 'favorite'
        })

    return render(request, "ProductApp/detail.html", context)


def locationfilter(request, search_word="empty", slug="empty"):
    _country = request.GET.get('country-input')
    _city = request.GET.get('city-input')
    _district = request.GET.get('district-input')
    _word = request.GET.get('filterby_word')

    return_dict = {}

    if _word:
        if slug != 'empty':
            if _city and _district:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(user__address__city__icontains=_city) & Q(user__address__district__icontains=_district) & Q(category__slug = slug) & Q(name__icontains=_word))
            elif _city:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(user__address__city__icontains=_city) & Q(category__slug = slug) & Q(name__icontains=_word))
            else:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(category__slug = slug) & Q(name__icontains=_word))
        else:
            if _city and _district:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(user__address__city__icontains=_city) & Q(user__address__district__icontains=_district) & Q(name__icontains = search_word) & Q(name__icontains=_word))
            elif _city:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(user__address__city__icontains=_city) & Q(name__icontains = search_word) & Q(name__icontains=_word))
            else:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(name__icontains = search_word) & Q(name__icontains=_word))
        return_dict.update({'filterby_word' : _word})

    else:
        if slug != 'empty':
            if _city and _district:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(user__address__city__icontains=_city) & Q(user__address__district__icontains=_district) & Q(category__slug = slug))
            elif _city:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(user__address__city__icontains=_city) & Q(category__slug = slug))
            else:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(category__slug = slug))

        else:
            if _city and _district:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(user__address__city__icontains=_city) & Q(user__address__district__icontains=_district) & Q(name__icontains = search_word))
            elif _city:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(user__address__city__icontains=_city) & Q(name__icontains = search_word))
            else:
                products = Product.objects.filter(Q(user__address__country__icontains=_country) & Q(name__icontains = search_word))

    s_city = str(_city)
    s_district = ", " + str(_district)

    if _district != None:
        location_str = s_city + s_district
        return_dict.update({'location_str' : location_str})
    elif _city != None: 
        location_str = s_city
        return_dict.update({'location_str' : location_str})
        

    return_dict.update({
        'products' : products,
        'country_name' : _country,
        'city_name' : _city,
        'district_name'  : _district,
    })
    return return_dict



def products(request, slug):
    products = Product.objects.filter(category__slug = slug)
    context = {
        "products" : products,
        "categories" : list(Category.objects.all())[:9],
        "slug" : slug,
        "title_name" : Category.objects.get(slug=slug).name,
    }

    if request.GET.get('country-input'):
        context.update(locationfilter(request, "this is search word", slug))
    elif request.GET.get('filterby_word'):
        _word = request.GET.get('filterby_word')
        filtered_products = set({})
        for product in products:
            if product.name.lower().find(_word.lower()) != -1:
                filtered_products.add(product)
        products = filtered_products
        context.update({'filterby_word' : _word})

    
    context.update({
        'product_length' : len(context['products'])
    })
    _products = context['products']
    paginator = Paginator(_products, 6)
    page_number = request.GET.get('page')
    _products = paginator.get_page(page_number)
    context.update({
        'products' : _products,
    })

    absolute_url = request.build_absolute_uri()
    searching_index = absolute_url.find('&page=')  
    if searching_index != -1:
        absolute_url = absolute_url[:searching_index]
    context.update({'absolute_url' : absolute_url})

    return render(request, "ProductApp/shop.html", context)

def search_product_company(request, search_word):
    context = {
        'categories' : Category.objects.all(),
        'title_name' : search_word,
    }
    if request.GET.get('country-input'):
        context.update(locationfilter(request, search_word))
    elif request.GET.get('filterby_word'):
        _word = request.GET.get('filterby_word')
        products = Product.objects.filter(Q(name__icontains = search_word) & Q(name__icontains = _word))
        context.update({'products':products, 'filterby_word' : _word})
    else:
        _word = search_word
        products = Product.objects.filter(Q(name__icontains=_word) | Q(user__name__icontains = _word))
        context.update({
            'products' : products, 
        })
    

    context.update({
        'product_length' : len(context['products'])
    })
    _products = context['products']
    paginator = Paginator(_products, 6)
    page_number = request.GET.get('page')
    _products = paginator.get_page(page_number)
    context.update({
        'products' : _products,
    })

    absolute_url = request.build_absolute_uri()
    searching_index = absolute_url.find('&page=')  
    if searching_index != -1:
        absolute_url = absolute_url[:searching_index]
    context.update({'absolute_url' : absolute_url})

    return render(request, "ProductApp/shop.html", context)
    
def location_auto_complete(request, country_word, city_word, district_word):
    with open('./static/data/iller_ilceler.json', 'r',  encoding='utf-8') as f:
        data = json.load(f)

    city_list = []
    district_list = []
    response_dict = {
        'city_list' : city_list,
        'district_list' : district_list
    }

    if city_word == '_empty_':
        response_dict['city_list'] = data 
    else: 
        for city_ in data:
            if city_['il'].lower().find(city_word.lower()) != -1:
                city_list.append(city_)

    if district_word != 'all!':
        if district_word == '_empty_':
            response_dict['district_list'] = city_list[0]['ilceleri']
        else: 
            for district_ in city_list[0]['ilceleri']:
                if district_.lower().find(district_word) != -1:
                    district_list.append(district_)

    return JsonResponse(response_dict)

def review_saver(request, review_type):

    if review_type == 'to-product':
        review_text = request.POST.get('review_to_product')
        slug = request.POST.get('current_product_slug')
        product = Product.objects.get(slug=slug)
        print(request.user.username)
        review = Review.objects.create(from_user = request.user, review_text = review_text, product = product)
        return HttpResponse('basarili')

    elif review_type == "to-seller":
        review_text = request.POST.get('review_to_seller')
        slug = request.POST.get('current_seller_slug')
        user = CustomUser.objects.get(slug=slug)
        print(request.user.username)
        review = Review.objects.create(from_user = request.user, review_text = review_text, to_user = user)
        return HttpResponse('basarili')


def favorites(request):
    products = Product.objects.filter(fav_user__username = request.user.username)

    context = {
        "products" : products,
        "categories" : list(Category.objects.all())[:9],
        "favorites" : "favorites",
        "title_name" : "Favori Ürünler Listeniz",
    }

    context.update({
        'product_length' : len(context['products'])
    })
    _products = context['products']
    paginator = Paginator(_products, 6)
    page_number = request.GET.get('page')
    _products = paginator.get_page(page_number)
    context.update({
        'products' : _products,
    })

    absolute_url = request.build_absolute_uri()
    searching_index = absolute_url.find('&page=')  
    if searching_index != -1:
        absolute_url = absolute_url[:searching_index]
    context.update({'absolute_url' : absolute_url})

    return render(request, 'ProductApp/shop.html', context)

def addfavorites(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user

    if user.username != '':
        try:
            product.fav_user.add(user)
        except:
            return JsonResponse({'error' : 'Ürünü favorilere eklerken bir hata oluştu.'})

        return JsonResponse({'success' : 'Ürün favorilere eklendi.'})
    else:
        return JsonResponse({'error' : 'Ürünü favorilere ekleyebilmek için önce giriş yapmalısınız.'})

def discardfavorites(request, slug):
    product = Product.objects.get(slug=slug)
    user = request.user

    try:
        product.fav_user.remove(user)
    except:
        return JsonResponse({'error' : 'Ürünü favorilerden çıkarırken bir hata oluştu.'})

    return JsonResponse({'success' : 'Ürün favorilerden çıkarıldı.'})

def add_product(request):

    user = request.user
    form = AddProductForm(request.POST, request.FILES)

    if form.is_valid():
        product = form.save()
        product.user = user
        product.save()
    

    return redirect('profilePage', user.slug)