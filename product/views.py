import requests
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .models import Category, Product
from django.utils.text import slugify


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
    context = {'product': product}
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
