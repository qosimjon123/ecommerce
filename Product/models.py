from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)





    def __str__(self):
        return self.name



class Store(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    delivery_radius_km = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand.name} - {self.address}"



class Category(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_index=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['brand_id']),
            models.Index(fields=['subcategory_id']),
        ]

class StoreProduct(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} в {self.store.address}"

    class Meta:
        unique_together = ('store', 'product')
        indexes = [
            models.Index(fields=['store_id']),
            models.Index(fields=['product_id']),
        ]

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    new_price = models.DecimalField(max_digits=10, decimal_places=2)
    old_discount = models.IntegerField()
    new_discount = models.IntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} в {self.store.address}"
