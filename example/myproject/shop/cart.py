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
        # Itemの内容をコピーしてCartItemのインスタンスを生成
        cart_item = CartItem(
            id=item.id, name=item.name, price=item.price, code=item.code
        )
        self.items.append(cart_item)

    def clear(self):
        """カートの中身を空にする"""
        self.items.clear()

    def to_data(self):
        """Cartインスタンスをセッション内に格納する辞書形式に変換する"""
        # Cart.itemsを辞書で変換 list[dict] の形になる
        return asdict(self)["items"]

    @classmethod
    def from_data(cls, lst):
        """セッション内に格納しておいたデータ list[dict] からCartインスタンスを作る"""
        cart = cls()
        for item_data in lst:
            cart_item = CartItem(**item_data)
            cart.add(cart_item)
        return cart

    @classmethod
    def from_session(cls, session_data, key):
        """セッションからカートを生成"""
        # Sessionインスタンス(辞書ライクなオブジェクト)からカートデータを取得
        cart_data = session_data.get(key)
        if cart_data:
            # 既存データがあれば Cart.from_data メソッドでCartインスタンスを復元
            cart = cls.from_data(cart_data)
        else:
            # 無ければ新規
            cart = cls()
        return cart

    def save_session(self, session_data, key):
        """カートをセッションに保存"""
        # Sessionインスタンスにキーを指定してカートのデータ list[dict] を代入
        session_data[key] = self.to_data()

    def __str__(self):
        return f"Cart:{self.items}"
