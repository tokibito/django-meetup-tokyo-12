from django.db import models


class Item(models.Model):
    """商品"""

    name = models.CharField("品名", max_length=50)
    price = models.PositiveIntegerField("価格", default=0)

    def __str__(self):
        return f"{self.pk}:{self.name}"
