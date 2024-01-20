from django.db import models


class Item(models.Model):
    """商品"""

    name = models.CharField("品名", max_length=50)
    price = models.PositiveIntegerField("価格", default=0)
    code = models.CharField("品番", max_length=4, default="0000")

    def __str__(self):
        return f"{self.pk}:{self.code}:{self.name}"


class OrderedItem(models.Model):
    """発注された商品"""
    name = models.CharField("品名", max_length=50)
    price = models.PositiveIntegerField("価格", default=0)
    code = models.CharField("品番", max_length=4, default="0000")

    def __str__(self):
        return f"{self.code}:{self.name}"


class PurchaseOrder(models.Model):
    """注文
    """
    from_name = models.CharField("注文者名", max_length=50)
    ordered_at = models.DateTimeField("注文日時", auto_now_add=True)
    ordered_items = models.ManyToManyField(OrderedItem, "発注に含まれる商品")
