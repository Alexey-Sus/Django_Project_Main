from django.shortcuts import render, get_object_or_404
from catalog.models import Product

# Create your views here.


def home(request):
    return render(request, 'home.html')


def contact_details(request):
    return render(request, 'contact_details.html')

#
# def product_details(request, product_id):
#     product = Product.objects.get(id=product_id)
#     context = {'product': product}
#     return render(request, 'product_details.html', context)


def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'product_details.html', context)


def prod_det_from_base(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'prod_det_from_base.html', context)


def main(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'main.html', context)


def upper_menu(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'upper_menu_subtempl.html', context)