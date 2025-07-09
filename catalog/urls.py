from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import NewappConfig
from django.conf import settings
from django.conf.urls.static import static
from catalog.views import (ContactDetailsTemplateView, ProductDetailView, ProdDetFromBaseDetailView,
                           ProductListView, UpperMenuListView, ProdDetFromBaseCreateView, ProductUpdateView,
                           ProductDeleteView, ProdFromCatListView)

app_name = NewappConfig.name

app_name = 'catalog'


urlpatterns = [
    path('contacts/', ContactDetailsTemplateView.as_view(), name='contact_details'),
    path('product_details/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_details'),
    path('prod_det_from_base/<int:pk>/', ProdDetFromBaseDetailView.as_view(), name='prod_det_from_base'),
    path('main/', cache_page(60)(ProductListView.as_view()), name='main'),
    path('upper_menu_subtempl/', UpperMenuListView.as_view(), name='upper_menu_subtempl'),
    path('prod_det_from_base_create/', ProdDetFromBaseCreateView.as_view(), name='prod_det_from_base_create'),
    path('product_update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product_delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('prod_list_from_cat/', ProdFromCatListView.as_view(), name='prod_list_from_cat'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
