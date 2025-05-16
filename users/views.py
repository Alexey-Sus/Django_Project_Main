from django.urls import reverse_lazy
from django.views.generic import CreateView
import logging
from users.forms import UserRegisterForm
from users.models import User

logger = logging.getLogger(__name__)

class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            logger.info("Form is valid")
            user = form.save()
            logger.info(f"User saved: {user.username}")
            return super().form_valid(form)
        else:
            logger.error("Form is invalid")
            logger.error(form.errors)
            print(form.errors)
            return super().form_invalid(form)
