from django.db import models

from member.models import Member
from product.managers import ProductManager


class Product(models.Model):
    product_name = models.CharField(max_length=3000, null=False, blank=False)
    product_price = models.IntegerField(null=False, default=0)
    product_count = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'tbl_product'
        ordering = ['-id']

