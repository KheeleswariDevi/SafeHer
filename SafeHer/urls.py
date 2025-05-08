from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import payment_view
from .views import edit_profile, view_profile



urlpatterns = [
    path('', views.index, name='index'),  
    path('tracking/', views.tracking, name='tracking'),  
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout_view, name='logout'), 
    path('hazardous_areas/', views.hazardous_areas_view, name='hazardous_areas_view'),
    path('hazardous_areas/report/', views.add_hazard_report, name='add_hazard_report'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('incognito/', views.incognito_mode, name='incognito_mode'),
    path('contact/', views.contact_us, name='contact_us'),
    path('submit_contact/', views.submit_contact, name='submit_contact'),  
    path('thank-you/', views.thank_you, name='thank_you'),  
    path('payment/', payment_view, name='payment')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

