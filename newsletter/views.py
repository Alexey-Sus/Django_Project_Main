from datetime import datetime

from django.contrib.auth import backends
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin
from users.models import User

from newsletter.models import Recipient, Message, Mailer, SendTry
from newsletter.forms import (RecipientForm, RecipientFormDelete, MessageForm, MessageFormDelete, MailerForm,
                              MailerDeleteForm, MailerFormManager, SendTryForm)
from users.forms import UserForm

import logging

logger = logging.getLogger(__name__)


class RecipientListView(ListView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'process_recipients.html'
    context_object_name = 'recipients'


class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'create_new_recipient.html'
    success_url = reverse_lazy('newsletter:process_recipients')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientDetailView(DetailView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'show_recipient.html'


class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = 'update_recipient.html'  # сделать новый шаблон для редактирования продукта
    success_url = reverse_lazy('newsletter:process_recipients')


class RecipientDeleteView(DeleteView):
    model = Recipient
    form_class = RecipientFormDelete
    template_name = 'delete_recipient.html'  # сделать новый шаблон для удаления продукта
    success_url = reverse_lazy('newsletter:process_recipients')


# прописываем все контроллеры для сообщений (Message)
class MessageListView(ListView):
    model = Message
    form_class = MessageForm
    template_name = 'process_messages.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'create_new_message.html'
    success_url = reverse_lazy('newsletter:process_messages')


class MessageDetailView(DetailView):
    model = Message
    form_class = MessageForm
    template_name = 'show_message.html'


class MessageDeleteView(DeleteView):
    model = Message
    form_class = MessageFormDelete
    template_name = 'delete_message.html'  # сделать новый шаблон для удаления продукта
    success_url = reverse_lazy('newsletter:process_messages')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'update_message.html'  # сделать новый шаблон для редактирования продукта
    success_url = reverse_lazy('newsletter:process_messages')


# создание контроллера для отправки рассылок получателям
class SendMailer(FormMixin, DetailView):
    model = Mailer
    template_name = 'send_mailers_on_demand.html'
    form_class = MailerForm
    success_url = reverse_lazy('newsletter:process_mailers')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.send_try_instance = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailer_pk = self.kwargs.get('pk')
        if mailer_pk:
            context['mailer'] = get_object_or_404(Mailer, pk=mailer_pk)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        mailer = form.save()

        if mailer.status != 'launched':
            self.send_try_instance = SendTry(newsletter=mailer, time_of_last_try=datetime.now(), status='failed')
            self.send_try_instance.save()
            self.send_mailer(mailer.pk, send_try=self.send_try_instance)

            mailer.status = 'launched'
            mailer.save()

        else:
            print(f'Рассылка с номером {mailer.pk} уже была отправлена. Сейчас отправки не будет.')
            return HttpResponseRedirect(self.get_success_url())

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        mailer_pk = self.kwargs.get('pk')

        if mailer_pk:
            mailer = Mailer.objects.get(pk=mailer_pk)

        if mailer.status != 'launched':
            self.send_try_instance = SendTry(newsletter=mailer, time_of_last_try=datetime.now(), status='failed')
            self.send_try_instance.save()
            self.send_mailer(mailer_pk, send_try=self.send_try_instance)

            mailer.status = 'launched'
            mailer.save()

        else:
            print(f'Рассылка с номером {mailer.pk} уже была отправлена. Сейчас отправки не будет.')
            return super().form_invalid(form)


        return super().form_invalid(form)

    def send_mailer(self, mailer_instance_id, send_try):
        mailer_instance = get_object_or_404(Mailer, pk=mailer_instance_id)
        subject = "Рассылка от нас"
        body = mailer_instance.message.message_body
        recipients = [recipient.email for recipient in mailer_instance.recipients.all()]

        try:
            send_mail(subject, body, 'asuspitsyn@mail.ru', recipients)
            print(f'Рассылка отправлена адресатам {mailer_instance.recipients}')
            send_try.number_of_success_tries += 1
            send_try.time_of_last_try = datetime.now()
            send_try.status = 'success'
            send_try.server_reply = backends.server_reply.message or 'OK'
            send_try.save()

            mailer_instance.status = 'ended'
            mailer_instance.save()

        except Exception as e:
            send_try.number_of_unsuccess_tries += 1
            send_try.time_of_last_try = datetime.now()
            send_try.status = 'failed'
            send_try.server_reply = str(e)
            send_try.save()

            mailer_instance.status = 'launched'
            mailer_instance.save()

            logger.error(f'Failed to send the mailer: {e}')


# class MailerListView(ListView):
#     model = Mailer
#     form_class = MailerForm
#     template_name = 'process_mailers.html'
#     context_object_name = 'mailers'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         mailers = Mailer.objects.all()
#         context['total_mailers'] = mailers.count()
#         context['active_mailers'] = mailers.filter(status='launched').count()
#         context['unique_recipients'] = Recipient.objects.values('email').distinct().count()
#         return context

class MailerListView(ListView):
    model = Mailer
    # form_class = MailerForm
    template_name = 'process_mailers.html'
    context_object_name = 'mailers'

    def get_queryset(self):

        if self.request.user.is_authenticated:

            if not self.request.user.is_news_manager:
                return Mailer.objects.filter(is_enabled=True)
            else:
                return Mailer.objects.all()
        else:
            return Mailer.objects.filter(is_enabled=False)


    def get_form_class(self):
        user = self.request.user

        if user.is_news_manager:
            return MailerFormManager
        else:
            return MailerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailers = Mailer.objects.all()
        context['total_mailers'] = mailers.count()
        context['active_mailers'] = mailers.filter(status='launched').count()
        context['unique_recipients'] = Recipient.objects.values('email').distinct().count()
        return context


class MailerDetailView(DetailView):
    model = Mailer
    form_class = MailerForm
    template_name = 'show_mailer.html'


# class MailerCreateView(CreateView):
class MailerCreateView(LoginRequiredMixin, CreateView):
    model = Mailer
    form_class = MailerForm
    template_name = 'create_new_mailer.html'
    success_url = reverse_lazy('newsletter:process_mailers')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailerDeleteView(DeleteView):
    model = Mailer
    form_class = MailerDeleteForm
    template_name = 'delete_mailer.html'
    success_url = reverse_lazy('newsletter:process_mailers')


class MailerUpdateView(UpdateView):
    model = Mailer
    form_class = MailerForm
    template_name = 'update_mailer.html'
    success_url = reverse_lazy('newsletter:process_mailers')


# блок контроллеров для работы с пользователями (CRUD)
class UserListView(ListView):
    model = User
    # form_class = UserForm
    template_name = 'process_users.html'
    context_object_name = 'users'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'update_user.html'
    success_url = reverse_lazy('newsletter:process_users')


class UserDetailView(DetailView):
    model = User
    template_name = 'show_user.html'


#прописываем контроллер для вывода попыток рассылок
class MailerTriesView(LoginRequiredMixin, ListView):
    model = SendTry
    template_name = 'show_mailer_tries.html'
    context_object_name = 'mailer__send_tries'
    login_url = '/users/login/'

def get_queryset(self):
    user = self.request.user

    if not user.is_authenticated:
        return redirect('login')

    elif user.is_news_manager:
        return SendTry.object.all()

    else:
        return SendTry.objects.all()

def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    send_tries = SendTry.objects.filter(owner=self.request.user)
    context['total_send_tries'] = send_tries.count()
    context['failed_send_tries'] = send_tries.filter(status='failed').count()
    context['succeeded_send_tries'] = send_tries.filter(status='success').count()
    return context

class MainPageView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mailers = Mailer.objects.all()
        context['total_mailers'] = mailers.count()
        context['active_mailers'] = mailers.filter(status='launched').count()
        context['unique_recipients'] = Recipient.objects.values('email').distinct().count()
        return context






