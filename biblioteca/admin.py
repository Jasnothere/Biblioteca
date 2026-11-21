from django.contrib import admin
from datetime import date
from .models import Categoria, Autor, Libro, Copia, Estudiante, Prestamo

# Register your models here.
admin.site.register(Categoria)
admin.site.register(Autor)

class PrestamoInline(admin.TabularInline):
    model = Prestamo
    extra = 1

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'correo_electronico']
    search_fields = ['nombre', 'codigo']
    inlines = [PrestamoInline]


class CopiaInline(admin.TabularInline):
    model = Copia      
    extra = 1          

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'isbn', 'anio_publicacion', 'categoria', 'idioma']
    search_fields = ['titulo', 'isbn']
    list_filter = ['categoria', 'idioma']
    inlines = [CopiaInline]


@admin.register(Copia)
class CopiaAdmin(admin.ModelAdmin):
    list_display = ['codigo_inventario', 'libro__titulo', 'condicion']
    search_fields = ['codigo_inventario', 'libro__titulo']
    list_filter = ['condicion']
    actions = ['marcar_dañada']
        
    @admin.action(description='Marcar como dañado')
    def marcar_dañada(self, request, queryset):
        cantidad = queryset.update(condicion='dañado')
        self.message_user(request, f'{cantidad} copia(s) marcadas como dañadas.')



@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ['estudiante__nombre', 'copia__codigo_inventario', 'fecha_prestamo', 'fecha_devolucion', 'fecha_limite']
    search_fields = ['estudiante__nombre', 'copia__codigo_inventario', 'estudiante__codigo']
    list_filter = ['fecha_prestamo', 'fecha_devolucion']
    readonly_fields = ['fecha_prestamo']
    actions = ['marcar_devuelto']
    
    @admin.action(description='Marcar como devuelto (hoy)')
    def marcar_devuelto(self, request, queryset):
        cantidad = queryset.filter(fecha_devolucion__isnull=True).update(fecha_devolucion=date.today())
        self.message_user(request, f'{cantidad} préstamo(s) marcados como devueltos.')