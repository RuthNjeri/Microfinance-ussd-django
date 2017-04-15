from django.conf.urls import url
from . import views


urlpatterns = [
      
      url(r'ussd$',views.callback, name = 'callback'),
      url(r'voice$',views.voice, name = 'voice'),
      url(r'menu$',views.menu, name = 'menu'),
      
      

]
