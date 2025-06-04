from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.generic import DetailView, TemplateView, ListView, UpdateView, DeleteView, CreateView
from catalog.models import Product
from catalog.forms import ProductForm, ProductFormDelete, ProductFormModerator
from django.urls import reverse_lazy
from catalog.services import ProdCatService

# инициализируем переменную со списком стоп-слов, чтобы использовать ее при создании формы
stop_words: list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                            'обман', 'полиция', 'радар']


class ContactDetailsTemplateView(TemplateView):
    template_name = 'contact_details.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    form_class = ProductForm
    template_name = 'product_details.html'

    def get_queryset(self):
        queryset = cache.get('product_detail_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('product_detail_queryset', queryset, 60 * 15)
        return queryset


class ProdDetFromBaseDetailView(LoginRequiredMixin, DetailView):
    model = Product
    form_class = ProductForm
    template_name = 'prod_det_from_base.html'
    template_name = 'prod_det_from_base.html'

#контроллер почти тот же самый, то есть, ProdDetFromBaseCreateView, с использованием формы, для создания
# продукта:

class ProdDetFromBaseCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'prod_det_from_base_create.html'
    success_url = reverse_lazy('catalog:main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['stop_words'] = stop_words  # передаем список stop_words в форму
        return kwargs

    def form_valid(self, form):
        # автоматическое присвоение текущего пользователя владельцу продукта
        form.instance.owner = self.request.user
        return super().form_valid(form)


#пишем контроллер для обновления информации по продукту
# class ProductUpdateView(UpdateView):
class ProductUpdateView(LoginRequiredMixin, UpdateView):

    model = Product
    form_class = ProductForm
    template_name = 'product_update.html' #сделать новый шаблон для редактирования продукта
    success_url = reverse_lazy('catalog:main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['stop_words'] = stop_words  # передаем список stop_words в форму
        return kwargs


    def get_form_class(self):
        user = self.request.user

        if user == self.object.owner and user.has_perm('catalog.can_unpublish_product'):
            return ProductFormModerator

        elif user.has_perm('catalog.can_unpublish_product'):
            return ProductFormModerator

        elif user == self.object.owner:
            return ProductForm

        else:
            raise PermissionDenied

# class ProductDeleteView(DeleteView):
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    form_class = ProductFormDelete
    template_name = 'product_delete.html'  # сделать новый шаблон для удаления продукта
    success_url = reverse_lazy('catalog:main')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.has_perm('catalog.can_delete_product'):
            return ProductFormDelete
        else:
            raise PermissionDenied

@method_decorator(cache_page(60 * 15), name='dispatch')
# class ProductListView(ListView):
class ProductListView(ListView):
    model = Product
    form_class = ProductForm
    template_name = 'main.html'
    context_object_name = 'products'

    def get_form_class(self):
        user = self.request.user

        if user.has_perm('catalog.can_unpublish_product'):
            return ProductFormModerator

        elif user == self.object.owner:
            return ProductForm

        else:
            return ProductForm


class UpperMenuListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'upper_menu_subtempl.html'
    context_object_name = 'products'

#пишем новое представление (контроллер) для списка продуктов из заданной категории
# class ProdFromCatListView(ListView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'prod_list_from_cat.html'
#
#     products = ProdCatService.get_products_from_category()  # забираем список прод. из из services.py
#     context = {'products': products}
#     context_object_name = 'products'
#
#     def get_queryset(self):
#         return ProdCatService.get_products_from_category()


class ProdFromCatListView(ListView):
    '''Кэшируем список продуктов из одной категории - низкоуровневое кэширование.
    Если кэша нет, достаем данные просто из БД.'''

    model = Product
    form_class = ProductForm
    template_name = 'prod_list_from_cat.html'

    products = ProdCatService.get_products_from_category()  # забираем список прод. из из services.py
    context = {'products': products}
    context_object_name = 'products'

    def get_queryset(self):
        queryset = cache.get('prod_cat_queryset')
        if not queryset:
            queryset = ProdCatService.get_products_from_category()
            cache.set('prod_cat_queryset', queryset, 60 * 15)
        return queryset





