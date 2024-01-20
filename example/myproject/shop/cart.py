from dataclasses import dataclass, field, asdict


@dataclass
class CartItem:
    """カート内の商品"""

    id: int
    name: str
    price: int
    code: str


@dataclass
class Cart:
    """ショッピングカートのクラス"""

    items: list[CartItem] = field(default_factory=list)

    def add(self, item):
        """商品を追加"""
        cart_item = CartItem(
            id=item.id, name=item.name, price=item.price, code=item.code
        )
        self.items.append(cart_item)

    def clear(self):
        self.items.clear()

    def to_data(self):
        return asdict(self)["items"]

    @classmethod
    def from_data(cls, lst):
        cart = cls()
        for item_data in lst:
            cart_item = CartItem(**item_data)
            cart.add(cart_item)
        return cart

    @classmethod
    def from_session(cls, session_data, key):
        cart_data = session_data.get(key)
        if cart_data:
            cart = cls.from_data(cart_data)
        else:
            cart = cls()
        return cart

    def save_session(self, session_data, key):
        session_data[key] = self.to_data()

    def __str__(self):
        return f"Cart:{self.items}"
