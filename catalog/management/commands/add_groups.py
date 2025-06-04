from django.core.management import BaseCommand
from django.contrib.auth.models import Group
from django.core import serializers


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        groups = Group.objects.filter(name__in=['Модератор продуктов', 'Контент-менеджер'])
        serialized_data = serializers.serialize('json', groups)
        with open('add_groups.json', 'w') as f:
            f.write(serialized_data)
        self.stdout.write(self.style.SUCCESS('Фикстуры для групп созданы успешно'))