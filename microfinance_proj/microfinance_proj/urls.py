from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^microfinance_callback/', include('microfinance_callback.url')),
]
