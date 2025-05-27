from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
import logging
from users.forms import UserRegisterForm
from users.models import User
import secrets
from config.settings import EMAIL_HOST_USER
from django.shortcuts import get_object_or_404, redirect

logger = logging.getLogger(__name__)

class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, подтверди свою почту для регистрации на сайте 127.0.0.1 - перейди по ссылке'
                    f' для подтверждения почты: {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)

def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


    # def form_valid(self, form):
    #     if form.is_valid():
    #         logger.info("Form is valid")
    #         user = form.save(commit=False)
    #         user.set_password(form.cleaned_data['password1'])
    #         user.save()
    #         logger.info(f"User saved: {user.username}")
    #         return super().form_valid(form)
    #     else:
    #         logger.error("Form is invalid")
    #         logger.error(form.errors)
    #         print(form.errors)
    #         return super().form_invalid(form)