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
            path('create_new_password/',views.create_new_password,name='create_new_password'),
            path('dashboard/',views.dashboard,name='dashboard'),
            path('contact_form',views.contact_form,name='contact_form'),
            path('signedup_course/<int:course_id>',views.signedup_course,name='signedup_course'),
            path('edit_profile',views.edit_profile,name='edit_profile'),
            path('change_password',views.change_password,name='change_password'),
            path('logout_user',views.logout_user,name='logout_user'),
            path('remove_course/<int:course_id>',views.remove_course,name='remove_course')
              ]