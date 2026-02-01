from django import forms
from newsletter.models import Recipient, Message, Mailer, SendTry


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ('email', 'full_name', 'comment')

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        #настройка атрибутов виджета для полей формы
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите email подписчика'})

        self.fields['full_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите его ФИО'})

        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите комментарий'})

class RecipientFormDelete(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = []


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('subject', 'message_body')

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        #настройка атрибутов виджета для полей формы
        self.fields['subject'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите тему cообщения'})

        self.fields['message_body'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите сообщение'})


class MessageFormDelete(forms.ModelForm):
    class Meta:
        model = Message
        fields = []


class MailerForm(forms.ModelForm):
    class Meta:
        model = Mailer
        fields = ['first_sending', 'message', 'recipients', 'status']

    def __init__(self, *args, stop_words=None, **kwargs):
        super(MailerForm, self).__init__(*args, **kwargs)
        self.stop_words = stop_words if stop_words is not None else []

        # настройка атрибутов виджета для полей формы
        self.fields['first_sending'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Введите дату начала отправки'})


class MailerFormManager(forms.ModelForm):
    class Meta:
        model = Mailer
        fields = ['message', 'recipients', 'is_enabled']


class MailerDeleteForm(forms.ModelForm):
    class Meta:
        model = Mailer
        fields = []


class MailerSendForm(forms.ModelForm):
    class Meta:
        model = Mailer
        fields = ['message']


class SendTryForm(forms.ModelForm):
    class Meta:
        model = SendTry
        fields = ['newsletter', 'status', 'server_reply']


