from pprint import pprint
from django.db import transaction
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import StoreProduct, Quantity
from .producer import SendToProducer


@receiver(post_save, sender=StoreProduct)
@receiver(post_save, sender=Quantity)
def synch_update_with_basket_api(sender, instance, created, **kwargs):
    data = []

    try:
            if sender == StoreProduct and created:
                Quantity.objects.create(store=instance)

            items = StoreProduct.objects.filter(
                Q(sent=False) | Q(quantity__sent=False)
            ).select_related('quantity').all()


            for item in items:

                raw = {
                        'store_id': item.store_id,
                        'product_id': item.product_id,
                        'sku': item.product.sku,
                        'price': float(item.price),
                        'discount': item.discount,
                        'quantity': item.quantity.quantity if hasattr(item, 'quantity') and item.quantity else 0
                    }
                data.append(raw)


            pprint(data)


            if data:


                try:
                    SendToProducer(data)
                    StoreProduct.objects.filter(sent=False).update(sent=True)
                    Quantity.objects.filter(sent=False).update(sent=True)
                except Exception as e:
                    print(f"Error sending to RabbitMQ: {e}")
                    raise e


    except Exception as e:
        print(f"Error in transaction: {e} ")







