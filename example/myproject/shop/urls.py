from django.urls import path
from . import views

urlpatterns = [
    path("", views.ItemListView.as_view(), name="item_list"),
    path(
        "add_to_cart/<int:item_id>", views.AddToCartView.as_view(), name="add_to_cart"
    ),
    path("clear_cart", views.ClearCartView.as_view(), name="clear_cart"),
]
