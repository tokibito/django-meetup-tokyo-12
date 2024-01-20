from django.contrib import admin
from . import models

admin.site.register(models.Item)
admin.site.register(models.OrderedItem)
admin.site.register(models.PurchaseOrder)
