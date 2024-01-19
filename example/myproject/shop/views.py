from django.views import generic
from django.urls import reverse_lazy
from .models import Item
from .cart import Cart

CART_SESSION_KEY = "cart"


class ItemListView(generic.ListView):
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.from_session(self.request.session, CART_SESSION_KEY)
        context.update({"cart": cart})
        return context


class AddToCartView(generic.RedirectView):
    url = reverse_lazy("item_list")

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=kwargs["item_id"])
        cart = Cart.from_session(request.session, CART_SESSION_KEY)
        cart.add(item)
        # セッション内のカートオブジェクトを更新
        cart.save_session(request.session, CART_SESSION_KEY)
        return super().get(request, *args, **kwargs)


class ClearCartView(generic.RedirectView):
    url = reverse_lazy("item_list")

    def get(self, request, *args, **kwargs):
        request.session.pop(CART_SESSION_KEY, None)
        return super().get(request, *args, **kwargs)
