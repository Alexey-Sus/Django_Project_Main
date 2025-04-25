from django.urls import path
from catalog.apps import NewappConfig
# from catalog.views import home, contact_details, product_details, main, prod_det_from_base, upper_menu
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import (ContactDetailsTemplateView, HomeTemplateView, ProductDetailView, ProdDetFromBaseDetailView,
                           ProductListView, UpperMenuListView)

app_name = NewappConfig.name

urlpatterns = [
    path('contacts/', ContactDetailsTemplateView.as_view(), name='contact_details'),
    path('home/', HomeTemplateView.as_view(), name='home'),
    path('product_details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('prod_det_from_base/<int:pk>/', ProdDetFromBaseDetailView.as_view(), name='prod_det_from_base'),
    path('main/', ProductListView.as_view(), name='main'),
    path('upper_menu_subtempl/', UpperMenuListView.as_view(), name='upper_menu_subtempl')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
