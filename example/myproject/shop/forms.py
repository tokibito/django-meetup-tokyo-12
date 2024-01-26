from django import forms
from .models import PurchaseOrder


class OrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = ["from_name"]
