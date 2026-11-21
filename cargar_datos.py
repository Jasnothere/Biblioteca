# Datos de prueba para la Fase 5 (Actividad Biblioteca UFPS)
# Uso: dentro de "python manage.py shell" ejecuta:
#   exec(open('cargar_datos.py', encoding='utf-8').read())
# Se puede ejecutar varias veces: get_or_create no duplica lo que ya existe.

from datetime import date, timedelta
from biblioteca.models import Categoria, Autor, Libro, Copia, Estudiante, Prestamo

hoy = date.today()

# ---------- Categorías ----------
novela, _ = Categoria.objects.get_or_create(nombre='Novela')
programacion, _ = Categoria.objects.get_or_create(nombre='Programación')
infantil, _ = Categoria.objects.get_or_create(nombre='Infantil')

# ---------- Autores ----------
gabo, _ = Autor.objects.get_or_create(nombre='Gabriel García Márquez')
martin, _ = Autor.objects.get_or_create(nombre='Robert C. Martin')
saint, _ = Autor.objects.get_or_create(nombre='Antoine de Saint-Exupéry')
matthes, _ = Autor.objects.get_or_create(nombre='Eric Matthes')


# ---------- Libros ----------
def crear_libro(isbn, titulo, anio, categoria, idioma, autor):
    libro, _ = Libro.objects.get_or_create(
        isbn=isbn,
        defaults={'titulo': titulo, 'anio_publicacion': anio,
                  'categoria': categoria, 'idioma': idioma},
    )
    libro.autor.add(autor)  # M2M: se agrega después de crear el libro
    return libro


cien = crear_libro('9780307474728', 'Cien años de soledad', 1967, novela, 'Español', gabo)
amor = crear_libro('9780307387264', 'El amor en los tiempos del cólera', 1985, novela, 'Español', gabo)
clean = crear_libro('9780132350884', 'Clean Code', 2008, programacion, 'Inglés', martin)
principito = crear_libro('9788478887194', 'El principito', 1943, infantil, 'Español', saint)
crash = crear_libro('9781593279288', 'Python Crash Course', 2019, programacion, 'Inglés', matthes)


# ---------- Copias ----------
def crear_copia(codigo, libro, condicion='NUEVO'):
    copia, _ = Copia.objects.get_or_create(
        codigo_inventario=codigo,
        defaults={'libro': libro, 'condicion': condicion},
    )
    return copia


c1 = crear_copia('INV-001', cien)
c2 = crear_copia('INV-002', cien, 'USADO')
c3 = crear_copia('INV-003', cien, 'DAÑADO')
c4 = crear_copia('INV-004', clean)
c5 = crear_copia('INV-005', clean, 'USADO')
c6 = crear_copia('INV-006', principito)
c7 = crear_copia('INV-007', principito, 'USADO')
c8 = crear_copia('INV-008', crash)
c9 = crear_copia('INV-009', amor)
c10 = crear_copia('INV-010', amor, 'DAÑADO')


# ---------- Estudiantes ----------
def crear_estudiante(codigo, nombre, correo):
    est, _ = Estudiante.objects.get_or_create(
        codigo=codigo,
        defaults={'nombre': nombre, 'correo_electronico': correo},
    )
    return est


ana = crear_estudiante('1001', 'Ana', 'ana@ufps.edu.co')
luis = crear_estudiante('1002', 'Luis', 'luis@ufps.edu.co')
carla = crear_estudiante('1003', 'Carla', 'carla@ufps.edu.co')
diego = crear_estudiante('1004', 'Diego', 'diego@ufps.edu.co')


# ---------- Préstamos ----------
# dias_atras: hace cuántos días se prestó
# plazo: días que tenía para devolverlo
# devuelto_hace: None = sigue sin devolver (préstamo activo)
def crear_prestamo(estudiante, copia, dias_atras, plazo, devuelto_hace=None):
    fecha = hoy - timedelta(days=dias_atras)
    prestamo, _ = Prestamo.objects.get_or_create(
        estudiante=estudiante, copia=copia, fecha_prestamo=fecha,
        defaults={
            'fecha_limite': fecha + timedelta(days=plazo),
            'fecha_devolucion': None if devuelto_hace is None else hoy - timedelta(days=devuelto_hace),
        },
    )
    return prestamo


crear_prestamo(ana, c4, dias_atras=20, plazo=14)                       # ACTIVO y VENCIDO
crear_prestamo(luis, c5, dias_atras=2, plazo=14)                       # activo, a tiempo
crear_prestamo(carla, c6, dias_atras=3, plazo=14)                      # activo, a tiempo
crear_prestamo(diego, c8, dias_atras=30, plazo=14, devuelto_hace=18)   # devuelto
crear_prestamo(carla, c9, dias_atras=40, plazo=14, devuelto_hace=25)   # devuelto
crear_prestamo(ana, c2, dias_atras=60, plazo=14, devuelto_hace=50)     # devuelto

print('Listo:')
print(' Libros:', Libro.objects.count())
print(' Autores:', Autor.objects.count())
print(' Copias:', Copia.objects.count())
print(' Estudiantes:', Estudiante.objects.count())
print(' Préstamos:', Prestamo.objects.count(),
      '| activos:', Prestamo.objects.filter(fecha_devolucion__isnull=True).count())
