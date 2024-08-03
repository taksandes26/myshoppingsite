import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Category, Product
from django.utils.text import slugify
from .recommender import Recommender
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'category': category, 'categories': categories, 'products': products}
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'products/list.html', context=context)


def product_detail(request, product_id, slug):
    product = get_object_or_404(Product, id=product_id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    key = "recently_viewed"
    recently_viewed_products = None
    if key in request.session:
        if product_id in request.session[key]:
            request.session[key].remove(product_id)
        request.session[key].insert(0, product_id)
        if len(request.session[key]) > 5:
            request.session[key].pop()
        print(request.session[key])
        recently_viewed_products = Product.objects.filter(id__in=request.session[key])

    else:
        # recently viewed 5 product
        request.session[key] = [product_id]
        # request.session['recently_viewed'] = ['3', '1', '2', '3', '4']
        print(request.session[key])

    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)

    context = {'product': product, "cart_product_form": cart_product_form, key: recently_viewed_products,
               'recommended_products': recommended_products}
    return render(request, 'products/detail.html', context=context)


def load_products(request):
    url = "https://fakestoreapi.com/products"
    response = requests.get(url=url)
    data = response.json()

    # save to db
    for item in data:
        category, created = Category.objects.get_or_create(name=item['category'], slug=slugify(item['category']))

        product = Product(
            category=category,
            name=item['title'],
            description=item['description'],
            price=item['price'],
            image_url=item['image'],
        )
        product.save()
