from django.conf.urls import url
from . import views


urlpatterns = [
      
      url(r'^$',views.callback, name = 'callback'),

]

# Create your views here.
