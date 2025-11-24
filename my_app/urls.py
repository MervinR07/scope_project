from django.urls import path
from . import views
urlpatterns=[path('home/',views.home,name='home'),
            path('aboutus/',views.aboutus,name='aboutus'),
            path('registration/',views.registration,name='registration'),
            path('contactus/',views.contactus,name='contactus'),
            path('scopelogin/',views.scopelogin,name='scopelogin'),
            path('forgot_password/',views.forgot_password,name='forgot_password'),
            path('first_time_login/',views.first_time_login,name='first_time_login'),
            path('verify/<uuid:token>/',views.verify,name='verify'),
            path('')
              ]