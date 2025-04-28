from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from catalog.models import Product


# def home(request):
#     return render(request, 'home.html')

class HomeTemplateView(TemplateView):
    template_name = 'home.html'


# def contact_details(request):
#     return render(request, 'contact_details.html')


class ContactDetailsTemplateView(TemplateView):
    template_name = 'contact_details.html'


# def product_details(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {'product': product}
#     return render(request, 'product_details.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'
    # здесь для context_object_name будет принято "product"


# def prod_det_from_base(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     context = {'product': product}
#     return render(request, 'prod_det_from_base.html', context)


class ProdDetFromBaseDetailView(DetailView):
    model = Product
    template_name = 'prod_det_from_base.html'
    # здесь для context_object_name будет принято "product"


# def main(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'main.html', context)


class ProductListView(ListView):
    model = Product
    template_name = 'main.html'
    context_object_name = 'products'


# def upper_menu(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'upper_menu_subtempl.html', context)


class UpperMenuListView(ListView):
    model = Product
    template_name = 'upper_menu_subtempl.html'
    context_object_name = 'products'