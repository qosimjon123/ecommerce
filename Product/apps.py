from django.apps import AppConfig


class ProductConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Product'

    def ready(self):
        import Product.signals
        from . import StreamConsumer
        StreamConsumer.start_consumer_pool()
