from django.shortcuts import render
from .cart import Cart
from django.shortcuts import get_object_or_404, redirect
from product.models import Product
from .forms import CartAddProductForm
from product.recommender import Recommender
from django.views.decorators.http import require_POST


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add_product(product=product, quantity=cd['quantity'], override_quantity=cd['override'])
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    cart_items = cart.get_cart_items()
    for item in cart_items:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    r = Recommender()
    cart_products = [item['product'] for item in cart_items]

    if cart_products:
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []

    return render(request, 'cart/detail.html', {'cart': cart, 'recommended_products': recommended_products})


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove_product(product)
    return redirect('cart:cart_detail')


def test_session(request):
    print(dir(request.session))
    # accessing data from session
    num_views = request.session.get("num_visit", 0)
    # storing data in session
    request.session["num_visit"] = num_views + 1
    # force django to update session
    request.session.modified = True
    # testing browser cookie
    request.session.set_test_cookie()
    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
    response = render(request, 'cart/test.html', {'visits': num_views})
    response.set_cookie("key", "value")
    response.set_cookie("name", "test_session")

    response.set_cookie("course", "django")

    return response

# ['TEST_COOKIE_NAME', 'TEST_COOKIE_VALUE', '_SessionBase__not_given', '_SessionBase__session_key',
# '__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__',
# '__format__', '__ge__', '__getattribute__', '__getitem__', '__getstate__', '__gt__', '__hash__',
# '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__',
# '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__',
# '__weakref__', '_get_new_session_key', '_get_or_create_session_key', '_get_session', '_get_session_from_db',
# '_get_session_key', '_session', '_session_key', '_set_session_key', '_validate_session_key', 'accessed', 'clear',
# 'clear_expired', 'create', 'create_model_instance', 'cycle_key', 'decode', 'delete', 'delete_test_cookie', 'encode',
# 'exists', 'flush', 'get', 'get_expire_at_browser_close', 'get_expiry_age', 'get_expiry_date', 'get_model_class',
# 'get_session_cookie_age', 'has_key', 'is_empty', 'items', 'key_salt', 'keys', 'load', 'model', 'modified', 'pop',
# 'save', 'serializer', 'session_key', 'set_expiry', 'set_test_cookie', 'setdefault', 'test_cookie_worked', 'update',
# 'values']
