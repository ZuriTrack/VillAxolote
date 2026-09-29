from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CarouselSlide, Biography, Product, Concert, News, SiteConfig


class VillAxoloteWebTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Crear un superusuario / admin
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='AdminPassword123!'
        )
        # Crear un usuario común / lector
        self.common_user = User.objects.create_user(
            username='lector_test',
            email='lector@test.com',
            password='UserPassword123!',
            is_staff=False,
            is_superuser=False
        )

        # Crear diapositiva de carrusel
        self.slide = CarouselSlide.objects.create(
            title="Slide de Prueba",
            subtitle="Subtítulo de prueba",
            order=1,
            is_active=True
        )

    def test_home_page_status_and_navbar(self):
        """Verificar que la página principal carga y contiene las 4 secciones clave."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        
        # 1. Biografía
        self.assertIn('Biografía', content)
        self.assertIn('#biografia', content)
        # 2. Tienda
        self.assertIn('Tienda', content)
        self.assertIn('#tienda', content)
        # 3. Conciertos y Noticias
        self.assertIn('Conciertos y Noticias', content)
        self.assertIn('#conciertos-noticias', content)
        # 4. Iniciar Sesión / Registro
        self.assertIn('Iniciar Sesión', content)
        self.assertIn('Registrarse', content)

    def test_anonymous_user_view(self):
        """El usuario no logueado no debe ver el botón de Panel Personalizado."""
        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')
        self.assertNotIn('Panel Personalizado', content)
        self.assertIn('Iniciar Sesión', content)

    def test_common_user_login_and_permissions(self):
        """El usuario común inicia sesión, ve su rol de Lector pero NO tiene el botón de administrar."""
        self.client.login(username='lector_test', password='UserPassword123!')
        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')
        
        self.assertIn('lector_test', content)
        self.assertIn('Lector', content)
        self.assertNotIn('Panel Personalizado', content)

    def test_common_user_blocked_from_custom_panel(self):
        """Un usuario común no puede acceder a /panel/, debe ser redirigido a home."""
        self.client.login(username='lector_test', password='UserPassword123!')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(response, reverse('home'))

    def test_anonymous_user_blocked_from_custom_panel(self):
        """Un visitante anónimo no puede acceder a /panel/, debe ser redirigido a login."""
        response = self.client.get(reverse('admin_dashboard'))
        self.assertRedirects(response, reverse('login'))

    def test_admin_user_login_unlocks_custom_panel(self):
        """El usuario administrador inicia sesión y se le desbloquea el botón 'Panel Personalizado'."""
        self.client.login(username='admin_test', password='AdminPassword123!')
        response = self.client.get(reverse('home'))
        content = response.content.decode('utf-8')
        
        self.assertIn('admin_test', content)
        self.assertIn('Admin', content)
        self.assertIn('Panel Personalizado', content)
        self.assertIn('/panel/', content)

    def test_admin_dashboard_renders(self):
        """El panel personalizado de control carga con código 200 para el administrador."""
        self.client.login(username='admin_test', password='AdminPassword123!')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Panel de Control Personalizado', content)
        self.assertIn('Diapositivas en Carrusel', content)
        self.assertIn('Productos en Tienda', content)

    def test_admin_can_create_product_in_custom_panel(self):
        """El admin puede crear un nuevo producto desde el panel personalizado."""
        self.client.login(username='admin_test', password='AdminPassword123!')
        # 1x1 pixel GIF válido para ImageField
        valid_gif = (
            b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
            b'\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00'
            b'\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
        )
        img = SimpleUploadedFile("test_pin.gif", valid_gif, content_type="image/gif")
        response = self.client.post(reverse('product_create'), {
            'name': 'Pin Axolote Dorado',
            'category': 'accesorios',
            'description': 'Pin esmaltado con acabado brillante',
            'price': '8.50',
            'badge': 'Nuevo',
            'stock': 30,
            'is_available': True,
            'image': img
        })
        self.assertRedirects(response, '/panel/?tab=tienda')
        self.assertTrue(Product.objects.filter(name='Pin Axolote Dorado').exists())

    def test_admin_can_edit_bio_in_custom_panel(self):
        """El admin puede editar la biografía desde el panel personalizado."""
        self.client.login(username='admin_test', password='AdminPassword123!')
        response = self.client.post(reverse('bio_edit'), {
            'title': 'Historia Actualizada de VillAxolote',
            'subtitle': 'Nueva Era',
            'body_1': 'Texto del nuevo inicio...',
            'body_2': 'Texto del segundo párrafo...',
            'quote': 'La magia continúa',
            'stat_1_number': '+200K',
            'stat_1_label': 'Fans',
            'stat_2_number': '60',
            'stat_2_label': 'Conciertos',
            'stat_3_number': '5',
            'stat_3_label': 'Discos'
        })
        self.assertRedirects(response, '/panel/?tab=biografia')
        bio = Biography.get_solo()
        self.assertEqual(bio.title, 'Historia Actualizada de VillAxolote')

    def test_registration_creates_reader_user(self):
        """Registrar una cuenta crea un usuario común (no staff)."""
        response = self.client.post(reverse('register'), {
            'username': 'nuevo_fan',
            'email': 'fan@axolotl.com',
            'password': 'Password123!',
            'password_confirm': 'Password123!'
        })
        self.assertRedirects(response, reverse('home'))
        new_user = User.objects.get(username='nuevo_fan')
        self.assertFalse(new_user.is_staff)
        self.assertFalse(new_user.is_superuser)
