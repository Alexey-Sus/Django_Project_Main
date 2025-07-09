from django.db import models
from users.models import User

class Recipient(models.Model):

    email = models.CharField(
        max_length=80, verbose_name="Эл. почта", unique=True,
    )
    full_name = models.CharField(
        max_length=150,
        verbose_name="ФИО получателя рассылки",
        blank=True,
        null=True,
    )

    comment = models.TextField(max_length=300, verbose_name='Комментарий')

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Этот подписчик создан пользователем: {self.owner.email}'

    def __str__(self):
        return self.email

class Message(models.Model):

    subject = models.CharField(max_length=100, verbose_name="Тема письма", help_text="Введите тему письма",)
    message_body = models.TextField(max_length=500, verbose_name="Тело письма", help_text="Введите сообщение",
                                    unique=True)
    # id = models.AutoField(primary_key=True, default='Сообщение')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject[:20]

# class Newsletter(models.Model):
#     STATUS_CHOICES = (('ended', 'Завершена'), ('created', 'Создана'), ('launched', 'Запущена'),)
#     status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='created')
#
#     date_send_start = models.DateField(auto_now=False, auto_now_add=False)
#     date_send_end = models.DateField(auto_now=False, auto_now_add=False)
#
#     message = models.ForeignKey(Message, on_delete=models.CASCADE, to_field='message_body', unique=True)
#     recipients = models.ManyToManyField(Recipient)
#
#     class Meta:
#         verbose_name = "Рассылка"
#         verbose_name_plural = "Рассылки"
#
#     def __str__(self):
#         return self.message[:20]


class Mailer(models.Model):

    first_sending = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                     help_text='Введите дату начала рассылки')

    final_sending = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True,
                                     help_text='Введите дату окончания рассылки')

    STATUS_CHOICES = (('ended', 'Завершена'), ('created', 'Создана'), ('launched', 'Запущена'),)

    # message = models.ForeignKey(Message, on_delete=models.CASCADE, to_field='message_body', unique=True)
    message = models.OneToOneField(Message, on_delete=models.CASCADE, to_field='message_body', unique=True)
    recipients = models.ManyToManyField(Recipient)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created')

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return self.message.message_body[:20]


class SendTry(models.Model):
    STATUS_CHOICES = (('success', 'Успешно'), ('failed', 'Безуспешно'),)

    time_of_last_try = models.DateField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='failed')
    server_reply = models.TextField(max_length=100)

    # newsletter = models.ForeignKey(Mailer, on_delete=models.CASCADE, to_field='message', unique=True)
    newsletter = models.OneToOneField(Mailer, on_delete=models.CASCADE, to_field='message', unique=True)

    number_of_success_tries = models.IntegerField(default=0)
    number_of_unsuccess_tries = models.IntegerField(default=0)


    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return self.newsletter[:20]



