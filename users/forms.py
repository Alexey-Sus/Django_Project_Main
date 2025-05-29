from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


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