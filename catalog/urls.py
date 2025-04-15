from django.urls import path
from catalog.apps import NewappConfig
from catalog.views import home, contact_details, product_details, main, prod_det_from_base, upper_menu
from django.conf import settings
from django.conf.urls.static import static

app_name = NewappConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contact_details, name='contact_details'),
    path('product_details/<int:pk>/', product_details, name='product_details'),
    path('prod_det_from_base/<int:pk>/', prod_det_from_base, name='prod_det_from_base'),
    path('main/', main, name='main'),
    path('upper_menu_subtempl/', upper_menu, name='upper_menu_subtempl'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
