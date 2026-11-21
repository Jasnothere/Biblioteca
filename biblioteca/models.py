from django.db import models
from django.db.models import Q
from datetime import date

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return f"Nombre Categoría: {self.nombre}"


class Autor(models.Model):
    nombre = models.CharField(max_length=60)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Nombre: {self.nombre}"


class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ManyToManyField(Autor, related_name='libros')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='libros')
    anio_publicacion = models.PositiveIntegerField()
    isbn = models.CharField(max_length=13, unique=True)
    idioma = models.CharField(max_length=30)

    def __str__(self):
        return f"Título: {self.titulo}, Anio de Publicación: {self.anio_publicacion}, ISBN: {self.isbn}"


class Copia(models.Model):

    CONDICIONES = [
        ('NUEVO', 'Nuevo'),
        ('USADO', 'Usado'),
        ('DAÑADO', 'Dañado'),
       
    ]

    libro = models.ForeignKey(Libro, on_delete=models.PROTECT, related_name='copias')
    codigo_inventario = models.CharField(max_length=20, unique=True)
    condicion = models.CharField(max_length=10, choices=CONDICIONES, default='NUEVO')

    def __str__(self):
        return f"Copia {self.codigo_inventario} de {self.libro.titulo} - Condición: {self.condicion}"


class Estudiante(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=60)
    correo_electronico = models.EmailField(unique=True)

    def __str__(self):
        return f"Estudiante: {self.nombre}, Correo: {self.correo_electronico}"


class Prestamo(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT, related_name='prestamos')
    copia = models.ForeignKey(Copia, on_delete=models.PROTECT, related_name='prestamos')
    fecha_prestamo = models.DateField(default=date.today)
    fecha_devolucion = models.DateField(null=True, blank=True)
    fecha_limite = models.DateField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['copia'],
                condition=Q(fecha_devolucion__isnull=True),
                name='una_copia_un_prestamo_activo',
                violation_error_message='Esta copia ya tiene un préstamo, activo y no puede ser prestada nuevamente hasta que sea devuelta.'
            )
        ]

    def __str__(self):
        return f"Préstamo de {self.copia.libro.titulo} a {self.estudiante.nombre} - {'Devuelto' if self.fecha_devolucion else 'Pendiente'}"