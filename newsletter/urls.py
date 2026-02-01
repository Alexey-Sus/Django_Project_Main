from django.urls import path
from django.views.decorators.cache import cache_page

from newsletter.apps import NewappConfig
from django.conf import settings
from django.conf.urls.static import static
from newsletter.views import (RecipientListView, RecipientCreateView, RecipientDetailView, RecipientUpdateView,
                              RecipientDeleteView, SendMailer, MailerListView, MailerDetailView, MailerCreateView,
                              MailerDeleteView, MailerUpdateView, UserListView, UserDetailView, UserUpdateView,
                              MessageListView, MessageCreateView, MessageDetailView, MessageDeleteView,
                              MessageUpdateView, MailerTriesView, MainPageView)

app_name = NewappConfig.name

app_name = 'newsletter'

urlpatterns = [
    path('process_recipients/', RecipientListView.as_view(), name='process_recipients'),
    path('create_new_recipient/', RecipientCreateView.as_view(), name='create_new_recipient'),
    path('show_recipient/<int:pk>/', RecipientDetailView.as_view(), name='show_recipient'),
    path('delete_recipient/<int:pk>/', RecipientDeleteView.as_view(), name='delete_recipient'),
    path('update_recipient/<int:pk>/', RecipientUpdateView.as_view(), name='update_recipient'),

    path('process_messages/', MessageListView.as_view(), name='process_messages'),
    path('create_new_message/', MessageCreateView.as_view(), name='create_new_message'),
    path('show_message/<int:pk>/', MessageDetailView.as_view(), name='show_message'),
    path('delete_message/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
    path('update_message/<int:pk>/', MessageUpdateView.as_view(), name='update_message'),

    path('send_mailers_on_demand/<int:pk>/', SendMailer.as_view(), name='send_mailers_on_demand'),
    path('process_mailers/', MailerListView.as_view(), name='process_mailers'),
    path('show_mailer/<int:pk>/', MailerDetailView.as_view(), name='show_mailer'),
    path('create_new_mailer/', MailerCreateView.as_view(), name='create_new_mailer'),
    path('delete_mailer/<int:pk>/', MailerDeleteView.as_view(), name='delete_mailer'),
    path('update_mailer/<int:pk>/', MailerUpdateView.as_view(), name='update_mailer'),

    path('process_users/', UserListView.as_view(), name='process_users'),
    path('show_user/<int:pk>/', UserDetailView.as_view(), name='show_user'),
    path('update_user/<int:pk>/', UserUpdateView.as_view(), name='update_user'),

    path('show_mailer_tries/', MailerTriesView.as_view(), name='show_mailer_tries'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
