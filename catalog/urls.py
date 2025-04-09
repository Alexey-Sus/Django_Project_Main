from django.urls import path
from catalog.apps import NewappConfig
from catalog.views import home, contact_details
from django.conf import settings
from django.conf.urls.static import static

app_name = NewappConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contact_details, name='contact_details')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
