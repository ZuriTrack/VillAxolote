from django.db import models
from django.utils import timezone


class CarouselSlide(models.Model):
    """
    Diapositivas para el carrusel principal administrable.
    """
    title = models.CharField(max_length=200, verbose_name="Título Principal")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Subtítulo o Descripción")
    image = models.ImageField(upload_to='carousel/', verbose_name="Imagen del Slide")
    button_text = models.CharField(max_length=60, blank=True, default="Descubrir más", verbose_name="Texto del Botón")
    button_link = models.CharField(max_length=255, blank=True, default="#biografia", verbose_name="Enlace del Botón")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden de aparición (menor a mayor)")
    is_active = models.BooleanField(default=True, verbose_name="¿Activo en el carrusel?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Diapositiva de Carrusel"
        verbose_name_plural = "Carrusel (Diapositivas)"
        ordering = ['order', '-id']

    def __str__(self):
        return f"[{self.order}] {self.title}"


class Biography(models.Model):
    """
    Información biográfica administrable.
    """
    title = models.CharField(max_length=200, default="La Historia de VillAxolote", verbose_name="Título")
    subtitle = models.CharField(max_length=300, default="Sonidos de ensueño nacidos desde las profundidades del lago místico", verbose_name="Subtítulo")
    body_1 = models.TextField(
        default=(
            "VillAxolote nació como un proyecto musical y artístico que fusiona melodías indie-pop, "
            "sintetizadores etéreos y la ternura milenaria del ajolote rosa. Con ritmos envolventes y "
            "letras que celebran la naturaleza, la introspección y el amor, hemos creado un refugio "
            "rosado donde cada nota se siente como un cálido abrazo acuático."
        ),
        verbose_name="Primer Párrafo"
    )
    body_2 = models.TextField(
        blank=True,
        default=(
            "A lo largo de los años, nuestra comunidad no ha dejado de crecer. Desde pequeños escenarios "
            "locales hasta grandes festivales, llevamos con orgullo la estética pastel, la protección de "
            "nuestra fauna y una puesta en escena inmersiva que transporta al público a un paraíso flotante."
        ),
        verbose_name="Segundo Párrafo"
    )
    image = models.ImageField(upload_to='bio/', blank=True, null=True, verbose_name="Foto de Biografía")
    quote = models.CharField(
        max_length=300,
        blank=True,
        default="«Nadar contra la corriente con dulzura, magia y pasión»",
        verbose_name="Frase o Cita Destacada"
    )
    stat_1_number = models.CharField(max_length=30, default="+120K", verbose_name="Dato 1 - Cifra")
    stat_1_label = models.CharField(max_length=100, default="Oyentes en Streaming", verbose_name="Dato 1 - Etiqueta")
    stat_2_number = models.CharField(max_length=30, default="48", verbose_name="Dato 2 - Cifra")
    stat_2_label = models.CharField(max_length=100, default="Conciertos Realizados", verbose_name="Dato 2 - Etiqueta")
    stat_3_number = models.CharField(max_length=30, default="3", verbose_name="Dato 3 - Cifra")
    stat_3_label = models.CharField(max_length=100, default="Discos Publicados", verbose_name="Dato 3 - Etiqueta")

    class Meta:
        verbose_name = "Sección de Biografía"
        verbose_name_plural = "Biografía (Información del Sitio)"

    def __str__(self):
        return self.title

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class Product(models.Model):
    """
    Productos para la sección de Tienda oficial.
    """
    CATEGORY_CHOICES = [
        ('ropa', '🌸 Ropa & Moda'),
        ('musica', '🎵 Vinilos & Álbumes'),
        ('coleccionables', '✨ Peluches & Coleccionables'),
        ('accesorios', '🎀 Accesorios & Stickers'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nombre del Producto")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='coleccionables', verbose_name="Categoría")
    description = models.TextField(verbose_name="Descripción del Producto")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio ($)")
    image = models.ImageField(upload_to='tienda/', verbose_name="Imagen del Producto")
    badge = models.CharField(max_length=50, blank=True, help_text="Ej: Nuevo, Edición Rosa, Más Vendido", verbose_name="Insignia Destacada")
    stock = models.PositiveIntegerField(default=15, verbose_name="Stock Disponible")
    is_available = models.BooleanField(default=True, verbose_name="¿Disponible para la venta?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto de Tienda"
        verbose_name_plural = "Tienda (Productos y Merch)"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Concert(models.Model):
    """
    Conciertos y presentaciones en vivo.
    """
    STATUS_CHOICES = [
        ('disponible', 'Entradas Disponibles 🎟️'),
        ('ultimas', 'Últimas Entradas 🔥'),
        ('agotado', 'Agotado 🚫'),
        ('proximo', 'Próximamente ⏳'),
    ]

    title = models.CharField(max_length=200, default="Tour Rosa Místico", verbose_name="Nombre del Show / Gira")
    city = models.CharField(max_length=120, verbose_name="Ciudad / País")
    venue = models.CharField(max_length=200, verbose_name="Recinto o Estadio")
    date = models.DateTimeField(verbose_name="Fecha y Hora del Evento")
    status = models.CharField(max_length=40, choices=STATUS_CHOICES, default='disponible', verbose_name="Estado de Entradas")
    ticket_link = models.CharField(max_length=300, blank=True, default="#", verbose_name="Enlace de Compra de Tickets")
    is_active = models.BooleanField(default=True, verbose_name="¿Mostrar en la web?")

    class Meta:
        verbose_name = "Concierto"
        verbose_name_plural = "Conciertos"
        ordering = ['date']

    def __str__(self):
        return f"{self.city} - {self.venue} ({self.date.strftime('%d/%m/%Y')})"


class News(models.Model):
    """
    Noticias y novedades sobre VillAxolote.
    """
    title = models.CharField(max_length=250, verbose_name="Título de la Noticia")
    summary = models.TextField(verbose_name="Resumen Breve")
    content = models.TextField(blank=True, verbose_name="Cuerpo Completo de la Noticia")
    image = models.ImageField(upload_to='noticias/', blank=True, null=True, verbose_name="Imagen de Portada")
    tag = models.CharField(max_length=50, default="Novedad", verbose_name="Etiqueta / Categoría")
    published_date = models.DateField(default=timezone.now, verbose_name="Fecha de Publicación")
    is_featured = models.BooleanField(default=False, verbose_name="¿Noticia destacada?")
    is_active = models.BooleanField(default=True, verbose_name="¿Publicada en el sitio?")

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ['-published_date', '-id']

    def __str__(self):
        return self.title


class SiteConfig(models.Model):
    """
    Configuración general administrable de VillAxolote.
    """
    site_name = models.CharField(max_length=100, default="VillAxolote", verbose_name="Nombre de la Web / Proyecto")
    slogan = models.CharField(max_length=250, default="El universo melódico y mágico del ajolote rosa", verbose_name="Eslogan")
    announcement_bar = models.CharField(max_length=250, blank=True, default="🌸 ¡Bienvenidos a VillAxolote! Explora nuestra música, tienda oficial y próximas fechas.", verbose_name="Barra de Anuncios Superior")
    contact_email = models.EmailField(default="contacto@villaxolote.com", verbose_name="Email de Contacto")
    instagram_url = models.URLField(blank=True, default="https://instagram.com", verbose_name="Instagram")
    spotify_url = models.URLField(blank=True, default="https://spotify.com", verbose_name="Spotify")
    youtube_url = models.URLField(blank=True, default="https://youtube.com", verbose_name="YouTube")
    tiktok_url = models.URLField(blank=True, default="https://tiktok.com", verbose_name="TikTok")
    footer_text = models.CharField(max_length=250, default="© 2026 VillAxolote. Todos los derechos reservados.", verbose_name="Texto del Pie de Página")

    class Meta:
        verbose_name = "Configuración General del Sitio"
        verbose_name_plural = "Configuración del Sitio"

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj
