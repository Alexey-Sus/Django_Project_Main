from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView, UpdateView, DeleteView, CreateView
from catalog.models import Product
from catalog.forms import ProductForm, ProductFormDelete
from django.urls import reverse_lazy

# инициализируем переменную со списком стоп-слов, чтобы использовать ее при создании формы
stop_words: list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                            'обман', 'полиция', 'радар']


class HomeTemplateView(TemplateView):
    template_name = 'home.html'


class ContactDetailsTemplateView(TemplateView):
    template_name = 'contact_details.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_details.html'


class ProdDetFromBaseDetailView(DetailView):
    model = Product
    template_name = 'prod_det_from_base.html'

#контроллер почти тот же самый, то есть, ProdDetFromBaseCreateView, с использованием формы, для создания
# продукта:
class ProdDetFromBaseCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'prod_det_from_base_create.html'
    success_url = reverse_lazy('catalog:main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['stop_words'] = stop_words  # передаем список stop_words в форму
        return kwargs

#пишем контроллер для обновления информации по продукту
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_update.html' #сделать новый шаблон для редактирования продукта
    success_url = reverse_lazy('catalog:main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['stop_words'] = stop_words  # передаем список stop_words в форму
        return kwargs

#пишу контроллер для удаления продукта
# class ProductDeleteView(DeleteView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'product_delete.html'  # сделать новый шаблон для удаления продукта
#     success_url = reverse_lazy('catalog:main')

class ProductDeleteView(DeleteView):
    model = Product
    form_class = ProductFormDelete
    template_name = 'product_delete.html'  # сделать новый шаблон для удаления продукта
    success_url = reverse_lazy('catalog:main')


class ProductListView(ListView):
    model = Product
    template_name = 'main.html'
    context_object_name = 'products'


class UpperMenuListView(ListView):
    model = Product
    template_name = 'upper_menu_subtempl.html'
    context_object_name = 'products'