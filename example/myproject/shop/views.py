from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Item, OrderedItem, PurchaseOrder
from .cart import Cart
from . import forms

# カートデータを保持しておくセッションキー
CART_SESSION_KEY = "cart"


def item_list_view(request):
    cart = Cart.from_session(request.session, CART_SESSION_KEY)
    context = {
        "cart": cart,
        "object_list": Item.objects.all(),
    }
    print(dict(request.session))
    return render(request, "shop/item_list.html", context)


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
        # カートのデータをセッションに保存
        cart.save_session(request.session, CART_SESSION_KEY)
        return super().get(request, *args, **kwargs)


class ClearCartView(generic.RedirectView):
    url = reverse_lazy("item_list")

    def get(self, request, *args, **kwargs):
        # セッションのカートデータを削除する
        request.session.pop(CART_SESSION_KEY, None)
        return super().get(request, *args, **kwargs)


class OrderFormView(generic.CreateView):
    model = PurchaseOrder
    fields = ["from_name"]
    # form_class = forms.OrderForm
    success_url = reverse_lazy("order_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_cart()
        context.update({"cart": cart})
        return context

    def get_cart(self):
        """カートをセッションから取得する"""
        cart = Cart.from_session(self.request.session, CART_SESSION_KEY)
        return cart

    def form_valid(self, form):
        self.object = form.save()
        # カートの内容からOrderedItemを作成して保存
        cart = self.get_cart()
        ordered_items = []
        for cart_item in cart.items:
            ordered_item = OrderedItem.objects.create(
                name=cart_item.name,
                price=cart_item.price,
                code=cart_item.code,
            )
            ordered_items.append(ordered_item)
        self.object.ordered_items.add(*ordered_items)
        # セッションのカートデータを削除する
        self.request.session.pop(CART_SESSION_KEY, None)
        return super().form_valid(form)


class OrderCompleteView(generic.TemplateView):
    template_name = "shop/complete.html"
