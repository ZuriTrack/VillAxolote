# 🌸 VillAxolote

> **Sitio web oficial y universo melódico del ajolote rosa.**  
> Desarrollado con Django, paleta de colores rosa pastel, carrusel interactivo dinámico, tienda oficial, cartelera de conciertos y **Panel de Administración 100% Personalizado**.

---

## ✨ Características Principales

- 🎠 **Carrusel de Fotos Interactivo:**
  - Navegación con clics (flechas laterales y puntos indicadores).
  - Transición automática cada 5 segundos y pausa al pasar el cursor.
  - Administrable desde el panel de control.
- 📖 **Sección de Biografía:**
  - Historia del proyecto, filosofía, imagen oficial, cita destacada y métricas en vivo.
- 🛍️ **Tienda Oficial:**
  - Catálogo de productos (Ropa, Vinilos, Peluches, Stickers).
  - Filtro dinámico por categoría en tiempo real sin recargas de página.
  - Insignias personalizadas y control de stock.
- 🎟️ **Conciertos y Noticias:**
  - Fechas de la gira con estados dinámicos (Disponibles, Últimas Entradas, Agotado).
  - Publicaciones y comunicados de prensa con etiquetas temáticas.
- ⚙️ **Panel de Administración Personalizado (`/panel/`):**
  - Todo el contenido e imágenes del sitio se pueden cambiar directamente desde un panel con la estética del sitio.
  - No requiere usar el panel estándar de Django.
- 🔐 **Sistema de Autenticación y Roles:**
  - **Usuario Común / Lector:** Registro libre, perfil de solo lectura sin acceso a funciones de edición.
  - **Administrador:** Al iniciar sesión se desbloquea el botón **"⚙️ Panel Personalizado"** y botones contextuales de edición rápida en cada sección.

---

## 🎨 Paleta de Colores
- **Principal:** Rosa Pastel (`#f8a5c2`, `#ffd1dc`, `#fff5f7`)
- **Acentos:** Frambuesa / Berry (`#88304e`, `#5e2439`) y Blush Suave (`#f78fb3`)

---

## 🚀 Instalación y Puesta en Marcha Local

### 1. Clonar el repositorio
```bash
git clone https://github.com/ZuriTrack/VillAxolote.git
cd VillAxolote
```

### 2. Crear y activar entorno virtual
```bash
# Windows
python -m venv env
.\env\Scripts\Activate.ps1

# Linux / macOS
python -m venv env
source env/bin/activate
```

### 3. Instalar dependencias
```bash
pip install django pillow
```

### 4. Aplicar migraciones
```bash
python manage.py migrate
```

### 5. (Opcional) Cargar datos iniciales de demostración
```bash
python populate_data.py
```

### 6. Iniciar el servidor
```bash
python manage.py runserver
```

Abre en tu navegador: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🧪 Pruebas Unitarias
Para correr la suite de pruebas del proyecto:
```bash
python manage.py test
```

---

*Desarrollado con 💖 para VillAxolote.*
