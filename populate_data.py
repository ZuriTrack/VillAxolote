import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from web.models import CarouselSlide, Biography, Product, Concert, News, SiteConfig
from django.core.files.base import ContentFile

def get_svg_slide_1():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <defs>
    <linearGradient id="bg1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffd1dc" />
      <stop offset="50%" stop-color="#f8a5c2" />
      <stop offset="100%" stop-color="#f391a0" />
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.6"/>
      <stop offset="100%" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="600" fill="url(#bg1)"/>
  <circle cx="950" cy="300" r="240" fill="url(#glow)"/>
  <circle cx="200" cy="150" r="80" fill="#ffffff" fill-opacity="0.2"/>
  <circle cx="350" cy="480" r="120" fill="#ffffff" fill-opacity="0.15"/>
  <circle cx="80" cy="500" r="40" fill="#ffffff" fill-opacity="0.25"/>

  <!-- Axolotl Character Art -->
  <g transform="translate(800, 180) scale(1.1)">
    <!-- Branchial frills (branquias) -->
    <path d="M40 70 C-10 40 -10 10 30 30 C10 0 40 -10 60 20 C60 -20 90 -10 90 30" fill="#e66767" opacity="0.85"/>
    <path d="M200 70 C250 40 250 10 210 30 C230 0 200 -10 180 20 C180 -20 150 -10 150 30" fill="#e66767" opacity="0.85"/>
    <!-- Head -->
    <ellipse cx="120" cy="90" rx="85" ry="65" fill="#fde2e4" stroke="#f4a2b2" stroke-width="4"/>
    <!-- Blush -->
    <circle cx="65" cy="105" r="16" fill="#f8a5c2" opacity="0.8"/>
    <circle cx="175" cy="105" r="16" fill="#f8a5c2" opacity="0.8"/>
    <!-- Eyes -->
    <circle cx="80" cy="85" r="9" fill="#5e2439"/>
    <circle cx="160" cy="85" r="9" fill="#5e2439"/>
    <circle cx="78" cy="82" r="3" fill="#ffffff"/>
    <circle cx="158" cy="82" r="3" fill="#ffffff"/>
    <!-- Smile -->
    <path d="M105 105 Q120 120 135 105" fill="none" stroke="#5e2439" stroke-width="4" stroke-linecap="round"/>
    <!-- Little paws -->
    <ellipse cx="90" cy="170" rx="16" ry="12" fill="#fde2e4"/>
    <ellipse cx="150" cy="170" rx="16" ry="12" fill="#fde2e4"/>
  </g>

  <!-- Typography Overlay -->
  <text x="100" y="260" font-family="'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="64" fill="#5e2439">
    VILLAXOLOTE
  </text>
  <text x="102" y="325" font-family="'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="28" fill="#88304e">
    Gira Mística 2026 • Pop Acuático &amp; Melodías Rosadas
  </text>
  <text x="102" y="375" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" fill="#6d3049">
    Siente la magia de nuestro hábitat sonoro. ¡Nuevas fechas anunciadas!
  </text>
  <!-- Sparkles -->
  <text x="520" y="210" font-size="34">✨</text>
  <text x="650" y="380" font-size="28">🌸</text>
  <text x="80" y="190" font-size="30">🎵</text>
</svg>"""

def get_svg_slide_2():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <defs>
    <linearGradient id="bg2" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#fbc7d4" />
      <stop offset="50%" stop-color="#9796f0" />
      <stop offset="100%" stop-color="#f8a5c2" />
    </linearGradient>
  </defs>
  <rect width="1200" height="600" fill="url(#bg2)"/>
  
  <g transform="translate(750, 130)">
    <!-- Vinyl record -->
    <circle cx="200" cy="180" r="150" fill="#2c2c54"/>
    <circle cx="200" cy="180" r="140" fill="none" stroke="#40407a" stroke-width="2"/>
    <circle cx="200" cy="180" r="110" fill="none" stroke="#40407a" stroke-width="2"/>
    <circle cx="200" cy="180" r="80" fill="none" stroke="#40407a" stroke-width="2"/>
    <circle cx="200" cy="180" r="50" fill="#f8a5c2"/>
    <circle cx="200" cy="180" r="12" fill="#fde2e4"/>
  </g>

  <text x="100" y="250" font-family="'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="58" fill="#ffffff">
    NUEVA COLECCIÓN OFICIAL
  </text>
  <text x="102" y="315" font-family="'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="28" fill="#fff0f5">
    Merch exclusivo, vinilos color pastel y peluches de edición limitada
  </text>
  <text x="102" y="365" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" fill="#fde2e4">
    Lleva un pedacito de VillAxolote a tu habitación. ¡Envíos a todo el país!
  </text>
  <text x="560" y="180" font-size="36">🎁</text>
  <text x="100" y="440" font-size="30">🛍️ 🌸 💖</text>
</svg>"""

def get_svg_slide_3():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <defs>
    <linearGradient id="bg3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff9a9e" />
      <stop offset="99%" stop-color="#fecfef" />
    </linearGradient>
  </defs>
  <rect width="1200" height="600" fill="url(#bg3)"/>
  
  <circle cx="900" cy="300" r="180" fill="#ffffff" fill-opacity="0.3"/>
  <text x="820" y="340" font-size="120">🎤</text>

  <text x="100" y="240" font-family="'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="60" fill="#4a1525">
    EN VIVO &amp; CONCIERTOS
  </text>
  <text x="102" y="310" font-family="'Segoe UI', Roboto, sans-serif" font-weight="600" font-size="28" fill="#6d1b33">
    Próxima parada: Festival Rosa en Santiago, CDMX y Buenos Aires
  </text>
  <text x="102" y="360" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" fill="#7a253f">
    Asegura tus entradas antes de que se agoten. ¡Experiencia VIP disponible!
  </text>
  <text x="540" y="220" font-size="40">✨</text>
  <text x="100" y="440" font-size="32">🎟️ ⚡ 🎶</text>
</svg>"""

def populate():
    print("Creando o actualizando configuración del sitio...")
    site_config = SiteConfig.get_solo()
    site_config.site_name = "VillAxolote"
    site_config.slogan = "Música, magia y estética anfibio-rosada"
    site_config.announcement_bar = "🌸 ¡Nuevo single 'Aguas Rosadas' ya en streaming! Explora la tienda y próximas fechas en vivo."
    site_config.contact_email = "contacto@villaxolote.com"
    site_config.save()

    print("Creando o actualizando biografía...")
    bio = Biography.get_solo()
    bio.title = "La Leyenda & Historia de VillAxolote"
    bio.subtitle = "Un viaje de sonidos acuáticos, ensueño pastel y protección del ajolote"
    bio.body_1 = (
        "VillAxolote nació bajo la luz de la luna en los canales míticos de Xochimilco y la inspiración "
        "de los sintetizadores retro de los años 80 y el indie contemporáneo. Más que una banda o un colectivo, "
        "VillAxolote es un santuario sensorial donde el color rosa pastel se convierte en estandarte de ternura, "
        "resiliencia y amor incondicional por los pequeños anfibios que son tesoro de nuestra tierra."
    )
    bio.body_2 = (
        "A través de cada concierto, canción y diseño exclusivo de nuestra tienda, buscamos conectar a una comunidad "
        "global de soñadores. Nos emociona recibirlos en este hogar rosado, donde cada oyente es parte de nuestra manada."
    )
    bio.quote = "«En un mundo ruidoso, elegimos la suavidad y la luz del ajolote rosa»"
    bio.stat_1_number = "+180K"
    bio.stat_1_label = "Oyentes Mensuales"
    bio.stat_2_number = "54"
    bio.stat_2_label = "Conciertos con Entradas Agotadas"
    bio.stat_3_number = "4"
    bio.stat_3_label = "Álbumes Publicados"
    bio.save()

    print("Creando Diapositivas de Carrusel...")
    if CarouselSlide.objects.count() == 0:
        s1 = CarouselSlide(
            title="VillAxolote: El Tour Rosa 2026",
            subtitle="Sumérgete en una experiencia multisensorial con visuales de ensueño y sonido envolvente.",
            button_text="Ver Conciertos 🎟️",
            button_link="#conciertos",
            order=1,
            is_active=True
        )
        s1.image.save("slide1.svg", ContentFile(get_svg_slide_1().encode('utf-8')), save=True)

        s2 = CarouselSlide(
            title="Tienda Oficial VillAxolote",
            subtitle="Peluches artesanales, polerones pastel, vinilos rosas y stickers impermeables para ti.",
            button_text="Explorar Tienda 🛍️",
            button_link="#tienda",
            order=2,
            is_active=True
        )
        s2.image.save("slide2.svg", ContentFile(get_svg_slide_2().encode('utf-8')), save=True)

        s3 = CarouselSlide(
            title="Nuestra Historia y Filosofía",
            subtitle="Descubre cómo nació el universo de VillAxolote y cómo apoyamos la preservación de la especie.",
            button_text="Leer Biografía 📖",
            button_link="#biografia",
            order=3,
            is_active=True
        )
        s3.image.save("slide3.svg", ContentFile(get_svg_slide_3().encode('utf-8')), save=True)
        print("Slides creadas con éxito.")
    else:
        print("Ya existen slides en la base de datos.")

    print("Creando Productos de muestra para la Tienda...")
    if Product.objects.count() == 0:
        def make_product_svg(title, icon, color):
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
                <rect width="400" height="400" rx="24" fill="{color}"/>
                <circle cx="200" cy="180" r="100" fill="#ffffff" fill-opacity="0.3"/>
                <text x="200" y="210" font-size="80" text-anchor="middle">{icon}</text>
                <text x="200" y="320" font-family="'Segoe UI', sans-serif" font-weight="bold" font-size="22" fill="#5e2439" text-anchor="middle">{title}</text>
            </svg>"""

        products_data = [
            ("Peluche Axolote Rosado Premium", "coleccionables", "Peluche ultrasuave de 35cm con branquias aterciopeladas y relleno antiestrés.", 24.99, "Más Vendido 🔥", 20, "🌸", "#ffd1dc"),
            ("Hoodie Pastel 'VillAxolote Sound'", "ropa", "Polerón con capucha 100% algodón orgánico peinado en suave rosa pastel con bordado frontal.", 45.00, "Nuevo ✨", 15, "👚", "#fbc7d4"),
            ("Vinilo 'Aguas Rosadas' (Edición Rosa Mármol)", "musica", "Prensado en vinilo translúcido de 180 gramos con libreto de arte e ilustraciones.", 32.50, "Edición Limitada 💎", 8, "🎵", "#f8a5c2"),
            ("Pack de 10 Stickers Holográficos de Ajolotes", "accesorios", "Stickers resistentes al agua y al sol con acabados tornasol y holográficos.", 9.99, "Favorito 🌟", 50, "✨", "#ffe5ec"),
            ("Gorra Bordada 'VillAxolote Dad Hat'", "ropa", "Gorra rosa pastel con correa ajustable metálica y bordado de ajolote en miniatura.", 19.99, "", 25, "🧢", "#fcd5ce"),
            ("Taza Cerámica 'Morning Axolotl'", "coleccionables", "Taza artesanal con orejitas esculpidas y capacidad de 400ml para tus cafés matutinos.", 14.50, "Regalo Ideal ☕", 18, "☕", "#fde2e4"),
        ]

        for name, cat, desc, price, badge, stock, icon, color in products_data:
            p = Product(name=name, category=cat, description=desc, price=price, badge=badge, stock=stock, is_available=True)
            p.image.save(f"prod_{name[:6].lower()}.svg", ContentFile(make_product_svg(name[:20], icon, color).encode('utf-8')), save=True)
        print("Productos de tienda creados con éxito.")
    else:
        print("Ya existen productos en la base de datos.")

    print("Creando Conciertos de muestra...")
    if Concert.objects.count() == 0:
        base_time = timezone.now()
        concerts_data = [
            ("Tour Rosa Místico", "Santiago, Chile", "Teatro Caupolicán", base_time + timedelta(days=14, hours=20), "ultimas", "#"),
            ("Festival Primavera Pastel", "Buenos Aires, Argentina", "Estadio Obras al Aire Libre", base_time + timedelta(days=28, hours=19), "disponible", "#"),
            ("Noche Acuática 2026", "Ciudad de México, México", "Auditorio BB", base_time + timedelta(days=45, hours=21), "disponible", "#"),
            ("Gira Acústica de Invierno", "Bogotá, Colombia", "Teatro Colón", base_time + timedelta(days=60, hours=20), "proximo", "#"),
            ("Gala Rosa Aniversario", "Lima, Perú", "Anfiteatro del Parque de la Exposición", base_time + timedelta(days=75, hours=19), "agotado", "#"),
        ]
        for title, city, venue, dt, status, link in concerts_data:
            Concert.objects.create(title=title, city=city, venue=venue, date=dt, status=status, ticket_link=link, is_active=True)
        print("Conciertos creados con éxito.")
    else:
        print("Ya existen conciertos en la base de datos.")

    print("Creando Noticias de muestra...")
    if News.objects.count() == 0:
        def make_news_svg(title, icon):
            return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 300" width="500" height="300">
                <defs>
                    <linearGradient id="nbg" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stop-color="#ffd1dc" />
                        <stop offset="100%" stop-color="#f8a5c2" />
                    </linearGradient>
                </defs>
                <rect width="500" height="300" rx="16" fill="url(#nbg)"/>
                <circle cx="250" cy="130" r="60" fill="#ffffff" fill-opacity="0.3"/>
                <text x="250" y="150" font-size="50" text-anchor="middle">{icon}</text>
                <text x="250" y="240" font-family="'Segoe UI', sans-serif" font-weight="bold" font-size="20" fill="#5e2439" text-anchor="middle">{title}</text>
            </svg>"""

        news_data = [
            (
                "¡Estrenamos el videoclip oficial de 'Burbujas Rosadas'!",
                "Un viaje animado cuadro a cuadro donde una familia de ajolotes descubre una ciudad de luces de neón rosa.",
                "El videoclip tomó más de 6 meses de trabajo junto a ilustradores independientes de Latinoamérica. Ya está disponible en nuestro canal oficial de YouTube y suma más de 250,000 reproducciones en sus primeras 48 horas.",
                "Estreno 🎬",
                True,
                "🎬"
            ),
            (
                "Iniciativa: Donamos el 10% de las ventas de la tienda al rescate del ajolote",
                "Nos aliamos con santuarios y centros de investigación biológica para la conservación del Ambystoma mexicanum.",
                "Cada vez que compras un peluche, vinilo o prenda en nuestra tienda oficial, estás contribuyendo de forma transparente y directa a la limpieza de aguas y preservación en hábitats naturales protegidos.",
                "Comunidad 💚",
                False,
                "🌿"
            ),
            (
                "Confirmada nuestra participación en el Festival Iberoamericano",
                "VillAxolote encabezará el escenario alternativo con una puesta en escena inmersiva nunca antes vista.",
                "Tendremos pantallas holográficas, pirotecnia de confeti biodegradable rosa y una banda ampliada con quinteto de cuerdas en vivo.",
                "Festival 🎤",
                False,
                "⭐"
            ),
        ]
        for title, summary, content, tag, featured, icon in news_data:
            n = News(title=title, summary=summary, content=content, tag=tag, is_featured=featured, is_active=True)
            n.image.save(f"news_{title[:6].lower()}.svg", ContentFile(make_news_svg(title[:22], icon).encode('utf-8')), save=True)
        print("Noticias creadas con éxito.")
    else:
        print("Ya existen noticias en la base de datos.")

if __name__ == '__main__':
    populate()
    print("¡Base de datos de VillAxolote inicializada con éxito!")
