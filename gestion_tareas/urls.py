from django.urls import path
from . import views

urlpatterns = [
    path('tareas/'                 , views.index , name="index_tareas"),
    path('crear-tarea/'            , views.create, name="create_tarea"),
    path('guardar-tarea/'          , views.save  , name="save_tarea"),
    path('ver-tarea/<int:id>/'     , views.view  , name="view_tarea"),
    path('eliminar-tarea/<int:id>/', views.delete, name="delete_tarea")
]
