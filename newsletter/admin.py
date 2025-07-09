from django.contrib import admin
from newsletter.models import Recipient, Message, Mailer, SendTry

admin.site.register(Recipient)
admin.site.register(Message)
admin.site.register(SendTry)
admin.site.register(Mailer)

# @admin.register(Mailer)
# class MailerAdmin(admin.ModelAdmin):
#     list_display = ('first_sending', 'final_sending', 'status', 'is_enabled')
#     fields = ['first_sending', 'final_sending', 'message', 'recipients', 'status', 'is_enabled']
