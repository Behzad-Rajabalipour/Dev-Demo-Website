from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'                          # .products ro ezafe mikonim chon addressesh taghir karde
    
    def ready(self):                                # ba in method mishe module ro ezafe konim be modulehaye default mesle models,admin,...
        from . import signals
        return super().ready()
    
    
