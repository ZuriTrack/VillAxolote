from django.contrib import admin
from django.utils.html import format_html
from .models import CarouselSlide, Biography, Product, Concert, News, SiteConfig

# Personalización del Panel de Administración de Django
admin.site.site_header = "🌸 VillAxolote - Panel de Administración"
admin.site.site_title = "VillAxolote Admin"
admin.site.index_title = "Gestor de Contenido y Configuración"


@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'preview_image', 'button_text', 'is_active', 'created_at')
    list_display_links = ('title',)
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'subtitle')
    list_filter = ('is_active',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 48px; border-radius: 8px; object-fit: cover; border: 1px solid #f8a5c2;" />', obj.image.url)
        return "Sin imagen"
    preview_image.short_description = "Vista previa"


@admin.register(Biography)
class BiographyAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'preview_image')

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 8px; object-fit: cover;" />', obj.image.url)
        return "Sin foto"
    preview_image.short_description = "Foto"

    def has_add_permission(self, request):
        # Limitar a un solo registro de biografía
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'badge', 'is_available', 'preview_image')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    list_editable = ('price', 'stock', 'is_available')

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 45px; border-radius: 6px; object-fit: cover;" />', obj.image.url)
        return "Sin imagen"
    preview_image.short_description = "Miniatura"


@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('date', 'title', 'city', 'venue', 'status', 'is_active')
    list_filter = ('status', 'is_active')
    search_fields = ('title', 'city', 'venue')
    list_editable = ('status', 'is_active')
    ordering = ('date',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'tag', 'published_date', 'is_featured', 'is_active', 'preview_image')
    list_filter = ('tag', 'is_featured', 'is_active', 'published_date')
    search_fields = ('title', 'summary', 'content')
    list_editable = ('is_featured', 'is_active')

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 45px; border-radius: 6px; object-fit: cover;" />', obj.image.url)
        return "Sin imagen"
    preview_image.short_description = "Portada"


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'slogan', 'contact_email')

    def has_add_permission(self, request):
        # Limitar a un solo registro de configuración general
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)
