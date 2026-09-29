from django import forms
from .models import CarouselSlide, Biography, Product, Concert, News, SiteConfig


class CarouselSlideForm(forms.ModelForm):
    class Meta:
        model = CarouselSlide
        fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'order', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título llamativo del slide'}),
            'subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Subtítulo o texto explicativo'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'button_text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: Ver Más, Comprar'}),
            'button_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: #tienda o una URL externa'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BiographyForm(forms.ModelForm):
    class Meta:
        model = Biography
        fields = [
            'title', 'subtitle', 'body_1', 'body_2', 'image', 'quote',
            'stat_1_number', 'stat_1_label',
            'stat_2_number', 'stat_2_label',
            'stat_3_number', 'stat_3_label'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'body_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'body_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'quote': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_1_number': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_1_label': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_2_number': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_2_label': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_3_number': forms.TextInput(attrs={'class': 'form-control'}),
            'stat_3_label': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'image', 'badge', 'stock', 'is_available']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción detallada'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'badge': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: Más Vendido, Edición Limitada'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ConcertForm(forms.ModelForm):
    class Meta:
        model = Concert
        fields = ['title', 'city', 'venue', 'date', 'status', 'ticket_link', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'ticket_link': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'URL de venta de entradas'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.date:
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'summary', 'content', 'image', 'tag', 'published_date', 'is_featured', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ej: Lanzamiento, Gira, Donación'}),
            'published_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.published_date:
            self.initial['published_date'] = self.instance.published_date.strftime('%Y-%m-%d')


class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = [
            'site_name', 'slogan', 'announcement_bar', 'contact_email',
            'instagram_url', 'spotify_url', 'youtube_url', 'tiktok_url', 'footer_text'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slogan': forms.TextInput(attrs={'class': 'form-control'}),
            'announcement_bar': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.URLInput(attrs={'class': 'form-control'}),
            'spotify_url': forms.URLInput(attrs={'class': 'form-control'}),
            'youtube_url': forms.URLInput(attrs={'class': 'form-control'}),
            'tiktok_url': forms.URLInput(attrs={'class': 'form-control'}),
            'footer_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
