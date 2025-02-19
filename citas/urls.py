# Configuración de URLs
from django.urls import path
from .views import  lista_citas, detalle_cita, crear_cita, delete_cita, update_cita

urlpatterns = [
    path('citas/eliminar/<int:cita_id>/', delete_cita, name='delete_cita'),
    path('citas/', lista_citas, name='lista_citas'),
    path('citas/<int:pk>/', detalle_cita, name='detalle_cita'),
    path('citas/crear/', crear_cita, name='crear_cita'),
     path('citas/actualizar/<int:cita_id>/', update_cita, name='update_cita'),
   # path('citas/<int:pk>/eliminar/', eliminar_cita, name='eliminar_cita'),
]
