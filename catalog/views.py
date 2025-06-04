from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, TemplateView, ListView, UpdateView, DeleteView, CreateView
from catalog.models import Product
from catalog.forms import ProductForm, ProductFormDelete, ProductFormModerator
from django.urls import reverse_lazy, reverse

# инициализируем переменную со списком стоп-слов, чтобы использовать ее при создании формы
stop_words: list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                            'обман', 'полиция', 'радар']


class ContactDetailsTemplateView(TemplateView):
    template_name = 'contact_details.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    form_class = ProductForm
    template_name = 'product_details.html'


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

    # def product_update(request, pk):
    #     product = get_object_or_404(Product, pk=pk)
    #     if request.method == 'POST':
    #         product.is_published = request.POST.get('is_published') == 'on'  # Convert checkbox value to boolean
    #         product.save()
    #         return redirect('catalog:main')  # Redirect to catalog:main AFTER saving.

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