from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'phone_number', 'is_blocked', 'is_news_manager', 'user_country')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        # настройка атрибутов виджета для полей формы
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Введите email пользователя'})

        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Укажите телефон'})

        self.fields['user_country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите страну'})


# class UserBlockForm(forms.Form):
#     user_id = forms.IntegerField(widget=forms.HiddenInput())
#     is_blocked = forms.BooleanField(required=False, label='Blocked')


# from django import forms
# from django.contrib.auth import get_user_model
# from django.contrib.auth.hashers import make_password
# from users.models import User
#
# User = get_user_model()
#
# class UserRegisterForm(forms.ModelForm):
#     password = forms.CharField(
#         label="Пароль",
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         required=True
#     )
#     password2 = forms.CharField(
#         label="Пароль еще раз",
#         widget=forms.PasswordInput(attrs={'class': 'form-control'}),
#         required=True
#     )
#
#     class Meta:
#         model = User
#         fields = ('email', 'password')  # Указываем только поле email
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError("Этот email уже зарегистрирован.")
#         return email
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         password2 = cleaned_data.get("password2")
#
#         if password != password2:
#             raise forms.ValidationError(
#                 "Пароли не совпадают"
#             )
#         return cleaned_data
#
#     def save(self, commit=True):
#         user = super().save(commit=False)  # Не сохраняем сразу, так как нужно захешировать пароль
#         user.password = make_password(self.cleaned_data['password'])  # Хешируем пароль
#         if commit:
#             user.save()
#         return user