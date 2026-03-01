from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('deposito/', views.deposito, name='deposito'),
    path('envio/', views.envio_dinero, name='envio_dinero'),
    path('transacciones/', views.transacciones, name='transacciones'),
    path('contactos/', views.contactos, name='contactos'),
    path('contactos/eliminar/<int:contact_id>/', views.eliminar_contacto, name='eliminar_contacto'),
]
