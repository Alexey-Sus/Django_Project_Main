from catalog.models import Product, Category

class ProdCatService:
    @staticmethod
    def get_products_from_category():

        try:
            category = Category.objects.get(name='Хлебобулочные изделия')  #берём какую-н. категорию
        except Category.DoesNotExist:
            return Product.objects.none()

        product_list = Product.objects.filter(category=category)
        return product_list