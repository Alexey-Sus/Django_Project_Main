from django.urls import path
from catalog.apps import NewappConfig
from catalog.views import home, contact_details


app_name = NewappConfig.name

urlpatterns = [
    path('home/', home, name='home'),
    path('contacts/', contact_details, name='contact_details')
]
