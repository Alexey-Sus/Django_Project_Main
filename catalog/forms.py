from django import forms
from django.core.exceptions import ValidationError
from catalog.models import Product

# создаем форму для ввода (создания) продукта
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image', 'purchase_price']

    def __init__(self, *args, stop_words=None, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.stop_words = stop_words if stop_words is not None else []

        #настройка атрибутов виджета для полей формы
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите навание продукта'})

        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите описание продукта'})

        self.fields['purchase_price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите цену продукта'})

    # определяем stop-слова для полей формы name и description
    # stop_words: list = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
    #                         'обман', 'полиция', 'радар']

    def clean_purchase_price(self):
        purchase_price: float = float(self.cleaned_data.get('purchase_price'))

        if purchase_price < 0:
            raise ValidationError(f'Неверный ввод цены "{purchase_price}". Цена должна быть больше или равна 0.')
        return purchase_price


    def clean_name(self):
        name: str = self.cleaned_data['name']

        for word in name.lower().split():
            if word in self.stop_words:
                raise ValidationError(f'Слово "{word}" не допускается ко вводу в названии')
        return name

    def clean_description(self):
        description: str = self.cleaned_data['description']

        for word in description.lower().split():
            if word in self.stop_words:
                raise ValidationError(f'Слово "{word}" не допускается ко вводу в описании товара')
        return description

# создадим специальную форму для удаления продукта(ов), поскольку в шаблоне нам не нужны поля для
# редактирования информации по продукту и созданию новых продуктов

class ProductFormDelete(forms.ModelForm):
    class Meta:
        model = Product
        fields = []



