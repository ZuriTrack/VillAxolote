from django.urls import path
from . import views

urlpatterns = [
    # Vistas Públicas
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # Panel de Administración Personalizado (Solo Admin)
    path('panel/', views.admin_dashboard, name='admin_dashboard'),

    # CRUD Carrusel
    path('panel/slide/add/', views.slide_create, name='slide_create'),
    path('panel/slide/<int:pk>/edit/', views.slide_edit, name='slide_edit'),
    path('panel/slide/<int:pk>/delete/', views.slide_delete, name='slide_delete'),

    # Biografía
    path('panel/bio/edit/', views.bio_edit, name='bio_edit'),

    # CRUD Tienda
    path('panel/product/add/', views.product_create, name='product_create'),
    path('panel/product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('panel/product/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # CRUD Conciertos
    path('panel/concert/add/', views.concert_create, name='concert_create'),
    path('panel/concert/<int:pk>/edit/', views.concert_edit, name='concert_edit'),
    path('panel/concert/<int:pk>/delete/', views.concert_delete, name='concert_delete'),

    # CRUD Noticias
    path('panel/news/add/', views.news_create, name='news_create'),
    path('panel/news/<int:pk>/edit/', views.news_edit, name='news_edit'),
    path('panel/news/<int:pk>/delete/', views.news_delete, name='news_delete'),

    # Configuración General
    path('panel/settings/edit/', views.site_config_edit, name='site_config_edit'),
]
