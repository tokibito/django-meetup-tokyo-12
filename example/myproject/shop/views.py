from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import Item, OrderedItem, PurchaseOrder
from .cart import Cart
from . import forms

# カートデータを保持しておくセッションキー
CART_SESSION_KEY = "cart"


def item_list_view(request):
    """商品一覧(関数ビュー)"""
    cart = Cart.from_session(request.session, CART_SESSION_KEY)
    context = {
        "cart": cart,
        "object_list": Item.objects.all(),
    }
    print(dict(request.session))
    return render(request, "shop/item_list.html", context)


class ItemListView(generic.ListView):
    """商品一覧(クラスベースビュー)"""
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # セッションからカートインスタンスを生成
        cart = Cart.from_session(self.request.session, CART_SESSION_KEY)
        context.update({"cart": cart})
        return context


class AddToCartView(generic.RedirectView):
    """商品をカートに追加"""
    url = reverse_lazy("item_list")

    def get(self, request, *args, **kwargs):
        item = Item.objects.get(id=kwargs["item_id"])
        # セッションからカートインスタンスを生成
        cart = Cart.from_session(request.session, CART_SESSION_KEY)
        cart.add(item)
        # カートのデータをセッションに保存
        cart.save_session(request.session, CART_SESSION_KEY)
        return super().get(request, *args, **kwargs)


class ClearCartView(generic.RedirectView):
    """カートを空にする"""
    url = reverse_lazy("item_list")

    def get(self, request, *args, **kwargs):
        # セッションのカートデータを削除する
        request.session.pop(CART_SESSION_KEY, None)
        return super().get(request, *args, **kwargs)


class OrderFormView(generic.CreateView):
    """注文フォーム"""
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
        """セッションからカートインスタンスを生成"""
        cart = Cart.from_session(self.request.session, CART_SESSION_KEY)
        return cart

    def form_valid(self, form):
        # フォームの保存(PurchaseOrderの保存)とインスタンスを保持
        self.object = form.save()
        # カートの内容からOrderedItemを作成して保存
        cart = self.get_cart()
        ordered_items = []
        for cart_item in cart.items:
            # カート内のCartItemの内容をコピーしてOrderedItemを作成、保存
            ordered_item = OrderedItem.objects.create(
                name=cart_item.name,
                price=cart_item.price,
                code=cart_item.code,
            )
            ordered_items.append(ordered_item)
        # PurchaseOrder.ordered_itemsにOrderedItemを追加
        self.object.ordered_items.add(*ordered_items)
        # セッションのカートデータを削除する
        self.request.session.pop(CART_SESSION_KEY, None)
        return super().form_valid(form)


class OrderCompleteView(generic.TemplateView):
    template_name = "shop/complete.html"
