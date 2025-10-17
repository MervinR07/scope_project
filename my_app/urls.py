from django.urls import path
from . import views
urlpatterns=[path('home/',views.home,name='home'),
            path('aboutus/',views.aboutus,name='aboutus'),
            path('registration/',views.registration,name='registration')
              ]