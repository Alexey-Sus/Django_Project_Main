from django.urls import path
from catalog.apps import NewappConfig
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import (ContactDetailsTemplateView, HomeTemplateView, ProductDetailView, ProdDetFromBaseDetailView,
                           ProductListView, UpperMenuListView, ProdDetFromBaseCreateView, ProductUpdateView,
                           ProductDeleteView)

app_name = NewappConfig.name

app_name = 'catalog'


urlpatterns = [
    path('contacts/', ContactDetailsTemplateView.as_view(), name='contact_details'),
    path('home/', HomeTemplateView.as_view(), name='home'),
    path('product_details/<int:pk>/', ProductDetailView.as_view(), name='product_details'),
    path('prod_det_from_base/<int:pk>/', ProdDetFromBaseDetailView.as_view(), name='prod_det_from_base'),
    path('main/', ProductListView.as_view(), name='main'),
    path('upper_menu_subtempl/', UpperMenuListView.as_view(), name='upper_menu_subtempl'),
    path('prod_det_from_base_create/', ProdDetFromBaseCreateView.as_view(), name='prod_det_from_base_create'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
