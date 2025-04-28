from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Add some test products to the database"

    def handle(self, *args, **options):

        Category.objects.all().delete()
        Product.objects.all().delete()

        category, _ = Category.objects.get_or_create(name="Канцтовары")
        test_products = [
            {
                "name": "Ручка гелевая",
                "description": "Ручка гелевая черная",
                "category": category,
                "purchase_price": 80.0,
            },
            {
                "name": "Линейка деревянная 30 см.",
                "description": "Линейка из сосновой древ. 30 см.",
                "category": category,
                "purchase_price": 110.0,
            },
            {
                "name": "Транспортир алюм.",
                "description": "Транспортир алюминиевый",
                "category": category,
                "purchase_price": 65.0,
            },
            {
                "name": "Тетрадь в клеточку 18 л.",
                "description": "Тетрадь в кл. 18 л., обложка зеленая",
                "category": category,
                "purchase_price": 30.0,
            },
            {
                "name": "Тетрадь в линейку 12 л.",
                "description": "Тетрадь в лин. без обл., 18 л.",
                "category": category,
                "purchase_price": 35.0,
            },
        ]

        for test_prod in test_products:
            product, created = Product.objects.get_or_create(**test_prod)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added product {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Product exists already: {product.name}")
                )
