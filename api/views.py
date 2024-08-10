from rest_framework import viewsets
from .serializer import UsuarioSerializer
from .models import Usuario

class UsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        # Obtener los parámetros desde los filtros
        usuario = self.request.query_params.get('usuario', None)
        clave = self.request.query_params.get('clave', None)
        nombre = self.request.query_params.get('nombre', None)
        rol = self.request.query_params.get('rol', None)
        estado = self.request.query_params.get('estado', None)

        # Crear un diccionario de los parámetros que no son None
        filters = {}
        if usuario is not None:
            filters['usuario'] = usuario
        if clave is not None:
            filters['clave'] = clave
        if nombre is not None:
            filters['nombre'] = nombre
        if rol is not None:
            filters['rol'] = rol
        if estado is not None:
            filters['estado'] = estado.lower() in ['true', '1', 't', 'yes', 'y']

        # Filtrar la queryset utilizando el diccionario de filtros
        if filters:
            return Usuario.objects.filter(**filters)
        else:
            return Usuario.objects.all()
