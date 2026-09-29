from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import CarouselSlide, Biography, Product, Concert, News, SiteConfig
from .forms import (
    CarouselSlideForm, BiographyForm, ProductForm,
    ConcertForm, NewsForm, SiteConfigForm
)


def admin_required(view_func):
    """
    Decorador para permitir el acceso ÚNICAMENTE a administradores (staff o superuser).
    Si un usuario común intenta entrar, se le bloquea y se le envía a la página principal.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión con una cuenta de Administrador para acceder al panel.")
            return redirect('login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Acceso Denegado: Tu cuenta tiene perfil de usuario común (solo lectura). No tienes permisos de administración.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ==============================================================================
# VISTAS PÚBLICAS
# ==============================================================================

def home(request):
    """
    Página principal de VillAxolote.
    """
    slides = CarouselSlide.objects.filter(is_active=True).order_by('order', '-id')
    bio = Biography.get_solo()
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    concerts = Concert.objects.filter(is_active=True).order_by('date')
    news_items = News.objects.filter(is_active=True).order_by('-published_date', '-id')
    site_config = SiteConfig.get_solo()

    is_admin = request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

    context = {
        'slides': slides,
        'bio': bio,
        'products': products,
        'concerts': concerts,
        'news_items': news_items,
        'site_config': site_config,
        'is_admin': is_admin,
    }
    return render(request, 'web/index.html', context)


def login_view(request):
    """
    Inicio de sesión con validación de rol.
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            try:
                user_obj = User.objects.get(email__iexact=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                messages.success(
                    request,
                    f"🌸 ¡Bienvenido Administrador @{user.username}! Se ha habilitado tu panel de administración personalizado."
                )
                return redirect('admin_dashboard')
            else:
                messages.success(
                    request,
                    f"💖 ¡Hola de nuevo, @{user.username}! Has iniciado sesión como miembro lector."
                )
                return redirect('home')
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos. Por favor intenta de nuevo.")

    site_config = SiteConfig.get_solo()
    return render(request, 'web/login.html', {'site_config': site_config})


def register_view(request):
    """
    Registro para miembros de la comunidad (usuarios lectores estándar).
    """
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()

        if not username or not password:
            messages.error(request, "El nombre de usuario y la contraseña son obligatorios.")
        elif password != password_confirm:
            messages.error(request, "Las contraseñas no coinciden.")
        elif len(password) < 6:
            messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
        elif User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Ese nombre de usuario ya está registrado.")
        elif email and User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Ese correo electrónico ya está registrado.")
        else:
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=False,
                is_superuser=False
            )
            login(request, new_user)
            messages.success(
                request,
                f"🎉 ¡Bienvenido a VillAxolote, @{new_user.username}! Tu cuenta ha sido creada como usuario lector."
            )
            return redirect('home')

    site_config = SiteConfig.get_solo()
    return render(request, 'web/register.html', {'site_config': site_config})


def logout_view(request):
    """
    Cierre de sesión.
    """
    if request.user.is_authenticated:
        username = request.user.username
        logout(request)
        messages.info(request, f"Hasta pronto, @{username}. ¡Vuelve cuando quieras!")
    return redirect('home')


# ==============================================================================
# PANEL DE ADMINISTRACIÓN PERSONALIZADO (Exclusivo para Admins)
# ==============================================================================

@admin_required
def admin_dashboard(request):
    """
    Vista principal del Panel de Administración personalizado con diseño rosa pastel.
    """
    active_tab = request.GET.get('tab', 'carrusel')

    slides = CarouselSlide.objects.all().order_by('order', '-id')
    bio = Biography.get_solo()
    products = Product.objects.all().order_by('-created_at')
    concerts = Concert.objects.all().order_by('date')
    news_items = News.objects.all().order_by('-published_date', '-id')
    site_config = SiteConfig.get_solo()

    context = {
        'active_tab': active_tab,
        'slides': slides,
        'bio': bio,
        'products': products,
        'concerts': concerts,
        'news_items': news_items,
        'site_config': site_config,
        'total_slides': slides.count(),
        'total_products': products.count(),
        'total_concerts': concerts.count(),
        'total_news': news_items.count(),
    }
    return render(request, 'web/panel/dashboard.html', context)


# --- CRUD CARRUSEL ---

@admin_required
def slide_create(request):
    if request.method == 'POST':
        form = CarouselSlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "🌸 Diapositiva agregada con éxito al carrusel.")
            return redirect('/panel/?tab=carrusel')
    else:
        form = CarouselSlideForm()

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': 'Agregar Nueva Diapositiva al Carrusel',
        'subtitle': 'Sube una imagen y define los textos que se verán en el slider de inicio',
        'back_tab': 'carrusel'
    })


@admin_required
def slide_edit(request, pk):
    slide = get_object_or_404(CarouselSlide, pk=pk)
    if request.method == 'POST':
        form = CarouselSlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            messages.success(request, f"🌸 Diapositiva #{slide.order} actualizada correctamente.")
            return redirect('/panel/?tab=carrusel')
    else:
        form = CarouselSlideForm(instance=slide)

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': f'Editar Diapositiva: {slide.title}',
        'subtitle': 'Modifica la imagen, el orden o los textos de este slide',
        'current_image': slide.image.url if slide.image else None,
        'back_tab': 'carrusel'
    })


@admin_required
def slide_delete(request, pk):
    slide = get_object_or_404(CarouselSlide, pk=pk)
    if request.method == 'POST':
        title = slide.title
        slide.delete()
        messages.success(request, f"🗑️ La diapositiva '{title}' fue eliminada del carrusel.")
    return redirect('/panel/?tab=carrusel')


# --- EDICIÓN BIOGRAFÍA ---

@admin_required
def bio_edit(request):
    bio = Biography.get_solo()
    if request.method == 'POST':
        form = BiographyForm(request.POST, request.FILES, instance=bio)
        if form.is_valid():
            form.save()
            messages.success(request, "🌸 Biografía y datos del sitio actualizados correctamente.")
            return redirect('/panel/?tab=biografia')
    else:
        form = BiographyForm(instance=bio)

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': 'Editar Biografía y Cifras de VillAxolote',
        'subtitle': 'Actualiza la historia, citas célebres, números destacados y la imagen principal',
        'current_image': bio.image.url if bio.image else None,
        'back_tab': 'biografia'
    })


# --- CRUD TIENDA / PRODUCTOS ---

@admin_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save()
            messages.success(request, f"🛍️ Producto '{p.name}' agregado a la tienda oficial.")
            return redirect('/panel/?tab=tienda')
    else:
        form = ProductForm()

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': 'Agregar Nuevo Producto a la Tienda',
        'subtitle': 'Establece el precio, foto, categoría e insignia destacada',
        'back_tab': 'tienda'
    })


@admin_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"🛍️ Producto '{product.name}' actualizado.")
            return redirect('/panel/?tab=tienda')
    else:
        form = ProductForm(instance=product)

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': f'Editar Producto: {product.name}',
        'subtitle': 'Actualiza los detalles, stock, precio o foto del producto',
        'current_image': product.image.url if product.image else None,
        'back_tab': 'tienda'
    })


@admin_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"🗑️ El producto '{name}' fue eliminado de la tienda.")
    return redirect('/panel/?tab=tienda')


# --- CRUD CONCIERTOS ---

@admin_required
def concert_create(request):
    if request.method == 'POST':
        form = ConcertForm(request.POST)
        if form.is_valid():
            c = form.save()
            messages.success(request, f"🎟️ Concierto en {c.city} agregado a la gira.")
            return redirect('/panel/?tab=conciertos')
    else:
        form = ConcertForm()

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': 'Agregar Fecha de Concierto / Show',
        'subtitle': 'Indica la ciudad, recinto, fecha, hora y enlace de venta de entradas',
        'back_tab': 'conciertos'
    })


@admin_required
def concert_edit(request, pk):
    concert = get_object_or_404(Concert, pk=pk)
    if request.method == 'POST':
        form = ConcertForm(request.POST, instance=concert)
        if form.is_valid():
            form.save()
            messages.success(request, f"🎟️ Fecha de concierto en {concert.city} actualizada.")
            return redirect('/panel/?tab=conciertos')
    else:
        form = ConcertForm(instance=concert)

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': f'Editar Concierto: {concert.city}',
        'subtitle': f'{concert.venue} - {concert.date.strftime("%d/%m/%Y")}',
        'back_tab': 'conciertos'
    })


@admin_required
def concert_delete(request, pk):
    concert = get_object_or_404(Concert, pk=pk)
    if request.method == 'POST':
        city = concert.city
        concert.delete()
        messages.success(request, f"🗑️ El concierto de {city} ha sido eliminado.")
    return redirect('/panel/?tab=conciertos')


# --- CRUD NOTICIAS ---

@admin_required
def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            n = form.save()
            messages.success(request, f"📰 Noticia '{n.title}' publicada.")
            return redirect('/panel/?tab=noticias')
    else:
        form = NewsForm()

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': 'Publicar Nueva Noticia / Novedad',
        'subtitle': 'Redacta un comunicado, agrega portada y etiqueta temática',
        'back_tab': 'noticias'
    })


@admin_required
def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            messages.success(request, f"📰 Noticia '{news.title}' actualizada.")
            return redirect('/panel/?tab=noticias')
    else:
        form = NewsForm(instance=news)

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': f'Editar Noticia: {news.title}',
        'subtitle': 'Modifica el contenido, resumen o imagen de portada',
        'current_image': news.image.url if news.image else None,
        'back_tab': 'noticias'
    })


@admin_required
def news_delete(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        title = news.title
        news.delete()
        messages.success(request, f"🗑️ La noticia '{title}' fue eliminada.")
    return redirect('/panel/?tab=noticias')


# --- CONFIGURACIÓN GENERAL DEL SITIO ---

@admin_required
def site_config_edit(request):
    config = SiteConfig.get_solo()
    if request.method == 'POST':
        form = SiteConfigForm(request.POST, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "🌸 Configuración general del sitio web actualizada con éxito.")
            return redirect('/panel/?tab=ajustes')
    else:
        form = SiteConfigForm(instance=config)

    return render(request, 'web/panel/form_page.html', {
        'form': form,
        'title': 'Configuración General de VillAxolote',
        'subtitle': 'Modifica el nombre, eslogan, redes sociales y textos de la web',
        'back_tab': 'ajustes'
    })
