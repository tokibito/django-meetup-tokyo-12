DjangoMeetupTokyo #12 中級者向けハンズオン
==========================================

イベント概要
------------

https://django.connpass.com/event/307423/

中級者向けハンズオンについて
----------------------------

チュートリアルは理解できている、Djangoは使ったことあるけど、使いこなせてない～という人向けのハンズオンです。 用意した資料を見ながら課題を実装していきます。

ショッピングカート、注文フォームの実装を通じて、Djangoのセッション、フォーム、汎用ビューなどの使い方を学びます。

作業環境の準備
--------------

* Python 3.12（Python3.10以上）
    * venvモジュールが使える状態にしてください。Ubuntuなどの環境では ``python3.12-venv`` のようなパッケージを入れる必要があるかもしれません。
    * ``python3.12 -m venv venv``
* Django 5.0系（最新 5.0.1）
    * venv環境にインストールしておいてください。
* VisualStudioCodeまたは、使い慣れたエディター
    * Python, Djangoで開発できる状態にしておいてください。

このハンズオンの完成形のコード
------------------------------

GitHub上に完成形のコードがあります。コードを書き進めていて、うまく動かない場合に参考にしてみてください。

https://github.com/tokibito/django-meetup-tokyo-12/

資料
----

https://tokibito.github.io/django-meetup-tokyo-12/

作成するアプリケーションについて
--------------------------------

ECサイトを想定したアプリケーションを作成します。

商品一覧ページ
~~~~~~~~~~~~~~~

データベースに登録しておいた商品一覧を表示するページです。

商品データはDjango adminからデータベースに登録する想定です。

ショッピングカート
~~~~~~~~~~~~~~~~~~~~

商品一覧ページで選んだ商品は、ショッピングカートに保持します。

ショッピングカートの内容は、一覧ページの下部に表示します。

注文フォームの機能
~~~~~~~~~~~~~~~~~~

注文データを作成するため、必要な情報を入力するフォームです。

ショッピングカートに入れた商品も表示します。

プロジェクトの作成とセットアップ
--------------------------------

Djangoのプロジェクト作成
~~~~~~~~~~~~~~~~~~~~~~~

今回は ``myproject`` という名前のプロジェクトで作成します。

.. code-block::

   (venv)$ django-admin startproject myproject
   (venv)$ cd myproject

**以降の説明は、このmyprojectディレクトリ以下を起点とします。**

管理者ユーザーの作成
~~~~~~~~~~~~~~~~~~~

Django管理サイト用のユーザーを作成しておきます。

.. code-block::

   (venv)$ python manage.py createsuperuser

django-debug-toolbarのセットアップ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

django-debug-toolbarをインストール、セットアップしておきます。

.. code-block::

   (venv)$ pip install django-debug-toolbar

.. note::

   - `django-debug-toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`_
   - `はじめてのDjangoアプリ作成、その8 | Django ドキュメント <https://docs.djangoproject.com/ja/5.0/intro/tutorial08/>`_

myproject/settings.py:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "debug_toolbar",
   ]

.. code-block:: python

   INTERNAL_IPS = [
       "127.0.0.1",
   ]

.. code-block:: python

   MIDDLEWARE = [
       "debug_toolbar.middleware.DebugToolbarMiddleware",
       # ...
   ]

.. note::

   ``DebugToolbarMiddleware`` は、なるべく外側に配置したほうがよいとドキュメントに書かれています。
   GZipMiddlewareのように、レスポンスボディを加工するミドルウェアを使っている場合は、それよりも後に配置する必要があります。
   DebugToolbarMiddlewareは、レスポンスのHTMLにscriptタグを差し込む処理を行っているためです。

myproject/urls.py:

.. code-block:: python

   from django.urls import include, path  # includeを追加しています

   urlpatterns = [
       # ...
       path("__debug__/", include("debug_toolbar.urls")),
   ]

これでdjango-debug-toolbarのセットアップまで完了です。初回のDBマイグレーションとrunserverで動作確認してください。

.. code-block::

   (venv)$ python manage.py migrate
   (venv)$ python manage.py runserver

http://127.0.0.1:8000/ をブラウザで開いて確認します。

shopアプリケーションを作成
---------------------------

.. code-block::

   (venv)$ python manage.py startapp shop

myproject/settings.py:

.. code-block:: python

   INSTALLED_APPS = [
       # ...
       "shop",
   ]

商品のモデルを作る
-------------------

shop/models.py:

.. code-block:: python

   from django.db import models


   class Item(models.Model):
       """商品"""

       name = models.CharField("品名", max_length=50)
       price = models.PositiveIntegerField("価格", default=0)
       code = models.CharField("品番", max_length=4, default="0000")

       def __str__(self):
           return f"Item:{self.pk}:{self.code}:{self.name}"

shop/admin.py:

.. code-block:: python

   from django.contrib import admin
   from . import models

   admin.site.register(models.Item)


マイグレーション
~~~~~~~~~~~~~~~

.. code-block::

   (venv)$ python manage.py makemigrations shop
   (venv)$ python manage.py migrate

商品一覧画面を作る
------------------

商品一覧画面を関数ビューで作ってみましょう。

shop/views.py:

.. code-block:: python

   from django.shortcuts import render
   from .models import Item

   def item_list_view(request):
       """商品一覧(関数ビュー)"""
       context = {
           "object_list": Item.objects.all(),
       }
       return render(request, "shop/item_list.html", context)

shop/urls.py(新規作成):

.. code-block:: python

   from django.urls import path
   from . import views

   urlpatterns = [
       path("", views.item_list_view, name="item_list"),
   ]

myproject/urls.py:

.. code-block:: python

   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path("admin/", admin.site.urls),
       path("", include("shop.urls")),
       path("__debug__/", include("debug_toolbar.urls")),
   ]

shop/templates/base.html(新規作成):

.. code-block:: html+django

   <html lang="ja">
   <head>
     <meta charset="utf-8">
     <title>{% block title %}{% endblock %}</title>
   </head>
   <body>
   {% block body %}{% endblock %}
   </body>
   </html>

shop/templates/shop/item_list.html(新規作成):

.. code-block:: html+django

   {% extends "base.html" %}

   {% block title %}商品一覧{% endblock %}

   {% block body %}
   <h1>商品一覧</h1>
   {% for item in object_list %}
   <div>
     {{ item.code }}:{{ item.name }} {{ item.price }}円
   </div>
   {% endfor %}
   {% endblock %}

ここまで作成したら、DjangoのadminからItemデータを追加し、 http://127.0.0.1:8000/ にアクセスして動作を確認してください。

クラスベースビューに変更する
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``item_list_view`` を関数ビューで作成しましたが、これを同等のクラスベースビューに変更してみましょう。

.. note::

   `クラスベースビュー | Django ドキュメント <https://docs.djangoproject.com/ja/5.0/topics/class-based-views/>`_

shop/views.py:

.. code-block:: python

   from django.views import generic
   from .models import Item

   class ItemListView(generic.ListView):
       """商品一覧(クラスベースビュー)"""

       model = Item

shop/urls.py:

.. code-block:: python

   from django.urls import path
   from . import views

   urlpatterns = [
       path("", views.ItemListView.as_view(), name="item_list"),
   ]

ここまで書き換えたら動作確認します。動作は関数ビューのときと同じになります。

ショッピングカートのクラスを作る
------------------------------

Pythonの標準モジュールであるdataclassesを使ってショッピングカートのクラスを実装します。

.. note::

   `dataclasses - データクラス — Python ドキュメント <https://docs.python.org/ja/3/library/dataclasses.html>`_

セッションに格納するデータ構造のイメージは以下の通りです。Pythonの ``list`` にカート内の商品情報を ``dict`` で複数格納します。

.. code-block::

   [
       {"id": 1, "name": "りんご", "price": 100, "code": "0001"},
   ]

カート内の商品は ``CartItem`` クラスで表現し、ショッピングカートは ``Cart`` クラスで表現します。
いずれも ``@dataclass`` デコレータを使用し、 ``asdict`` 関数を使って辞書に変換できるようにしておきます。

また、ショッピングカートをDjangoのセッションに格納、セッションから復元するためのメソッドも実装しておきます。

shop/cart.py:

.. code-block:: python

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

これでショッピングカートを表現するクラスを実装できました。

Djangoのシェルで動作を見てみましょう。

.. code-block:: pycon

   (venv)$ python manage.py shell
   >>> from shop.cart import CartItem, Cart
   >>> cart = Cart()
   >>> cart
   Cart(items=[])
   >>> item1 = CartItem(id=1, name="りんご", price=100, code="0001")
   >>> item1
   CartItem(id=1, name='りんご', price=100, code='0001')
   >>> cart.add(item1)
   >>> cart
   Cart(items=[CartItem(id=1, name='りんご', price=100, code='0001')])
   >>> cart.to_data()  # このメソッドの出力内容をDjangoのセッションに格納する
   [{'id': 1, 'name': 'りんご', 'price': 100, 'code': '0001'}]

   # Cart.from_data()により、Cartインスタンスを復元する
   >>> cart2 = Cart.from_data([{'id': 1, 'name': 'りんご', 'price': 100, 'code': '0001'}])
   >>> cart2
   Cart(items=[CartItem(id=1, name='りんご', price=100, code='0001')])

ショッピングカートに追加するビュー
--------------------------------

ショッピングカートに商品を追加するビューを実装します。 ``/add_to_cart/<Item.id>`` のようなURLで実装します。

このURLにGETリクエストでアクセスしたあとは、一覧画面にリダイレクトします。

shop/views.py:

.. code-block:: python

   # ...
   from django.urls import reverse_lazy
   from .cart import Cart

   # カートデータを保持しておくセッションキー
   CART_SESSION_KEY = "cart"

   # ...
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

``cart`` という名前のセッションキーで、Djangoのセッションに値を保存しています。

.. note::

   **django.urlsのreverse, reverse_lazyの使い分け**

   reverse関数、reverse_lazy関数の使い分けですが、モジュールを読み込んだときに評価される部分（クラス定義での変数代入）ではreverse_lazy、関数やクラスのメソッド内ではreverseを使うようにします。

   .. code-block:: python

      class Foo:
          bar = reverse_lazy("url_name")  # ここはモジュールを読み込んだときに関数が実行されるので、遅延評価のreverse_lazyを使う

          def foo(self):
              bar = reverse("url_name")  # ここはfooメソッド呼び出し時に関数が呼ばれるのでrevserseでよい

      def foo():
          bar = reverse("url_name")  # ここはfoo関数呼び出し時に関数が呼ばれるのでrevserseでよい

shop/urls.py:

.. code-block:: python

   from django.urls import path
   from . import views

   urlpatterns = [
       # ...
       path(
           "add_to_cart/<int:item_id>", views.AddToCartView.as_view(), name="add_to_cart"
       ),
   ]

このコードの動作確認はしづらいので、一旦そのまま次に進みましょう。

カートの中身を表示する
--------------------------------

カートの中身を表示できるように、 ``ItemListView`` を改修します。
``get_context_data`` を追加実装し、セッションからCartインスタンスを生成して、テンプレートにコンテキスト変数で渡します。

shop/views.py:

.. code-block:: python

   # ...

   class ItemListView(generic.ListView):
       """商品一覧(クラスベースビュー)"""

       model = Item

       def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           # セッションからカートインスタンスを生成
           cart = Cart.from_session(self.request.session, CART_SESSION_KEY)
           context.update({"cart": cart})
           return context

   # ...

テンプレートでは、 ``cart.items`` から取り出した ``CartItem`` インスタンスの内容を表示します。

このテンプレートの改修と一緒に、「カートに追加」のリンクも追加しておきます。

shop/templates/shop/item_list.html:

.. code-block:: html+django

   {% extends "base.html" %}

   {% block title %}商品一覧{% endblock %}

   {% block body %}
   <h1>商品一覧</h1>
   {% for item in object_list %}
   <div>
     {{ item.code }}:{{ item.name }} {{ item.price }}円
     <a href="{% url 'add_to_cart' item_id=item.id %}">カートに追加</a>
   </div>
   {% endfor %}
   <h2>カート内の商品</h2>
   {% for cart_item in cart.items %}
   <div>{{ cart_item.code }}:{{ cart_item.name }} {{ cart_item.price }}円</div>
   {% endfor %}
   {% endblock %}

ここまで書けたら、動作確認してみてください。カートに商品を追加できるようになるはずです。

セッション内のデータは、DebugToolbarを使うと確認が簡単です。

Djangoのセッションについて
~~~~~~~~~~~~~~~~~~~~~~~~~~

`セッションの使いかた | Django ドキュメント <https://docs.djangoproject.com/ja/5.0/topics/http/sessions/>`_

Djangoのセッションは、ビューの中で利用できます。

辞書ライクなオブジェクトなので、キーを指定して値を代入、参照できます。

関数ビューの場合:

.. code-block:: python

   def my_view(request):
       # セッションから my-data-key というキーで格納された値を取り出し
       data = request.session.get("my-data-key")
       # セッションに my-data-key というキーで辞書を格納
       request.session["my-data-key"] = {"foo": 123, "bar": "hoge"}

セッションに格納したデータは、有効期限が切れるまではページ遷移をしても保持されます。

``request.session`` に値を代入したり、内容を更新した場合、 ``SessionMiddleware`` が変更を検知してセッションの内容をデータベース等に保存します。

Djangoの認証機能のユーザー情報もセッションに格納されます。

一般的に、HTTPでセッション機能を実現するためには、異なる2つのリクエストが、同一の利用者（ブラウザ）からアクセスしてきたことを識別する必要があります。

Djangoの場合は、セッションIDを文字列で発行し、Cookieに格納しています。ブラウザから送信されたCookieからセッションIDを取り出し、サーバー側で既存のセッションIDと照合することで、同一性を確認しています。

.. note::

   - デフォルトの設定では、Djangoのセッションデータはデータベースに格納されます。 settings.SESSION_ENGINE で保存先を変更できます。

カートの中身をすべて消すビュー
--------------------------------

カートの中身を削除したい場合は、セッションからカートのデータを削除します。

セッションからキーを削除すると、キーが無い状態のセッションデータが保持されるため、削除相当の動作になります。

削除後は商品一覧画面にリダイレクトします。

shop/views.py:

.. code-block:: python

   class ClearCartView(generic.RedirectView):
       """カートを空にする"""

       url = reverse_lazy("item_list")

       def get(self, request, *args, **kwargs):
           # セッションのカートデータを削除する
           request.session.pop(CART_SESSION_KEY, None)
           return super().get(request, *args, **kwargs)

shop/urls.py:

.. code-block:: python

   # ...
   urlpatterns = [
       # ...
       path("clear_cart", views.ClearCartView.as_view(), name="clear_cart"),
   ]

shop/templates/shop/item_list.html:

.. code-block:: html+django

   {% block body %}
   # ...
   <a href="{% url 'clear_cart' %}">カートを空にする</a>
   {% endblock %}

ここまで実装したら動作確認しましょう。

カートに商品を追加する、カートをクリアする、といった機能を持つ基本的なショッピングカートの機能を実装できたことになります。

発注のモデルを作る
--------------------------------

さて、カートに入れた内容を発注する、といった想定で、発注の情報を入力し、データベースに格納する機能を作っていきます。

要件によりますが、発注後に商品の価格や名称を変更した場合、発注済みのデータも価格が変わってしまうと困る場合が多いと思います。
今回は、発注処理を行った時点の商品の情報をデータベースに格納するように実装します。

１つの注文には、商品が複数含まれます。 ``PurchaseOrder`` クラスで「発注」を表現し、 ``OrderedItem`` クラスで「発注に含まれる商品データ」を表現します。

注文のデータには、注文者名と注文日時を保存できるように作ってみます。

shop/models.py:

.. code-block:: python

   # ...

   class OrderedItem(models.Model):
       """発注された商品"""

       name = models.CharField("品名", max_length=50)
       price = models.PositiveIntegerField("価格", default=0)
       code = models.CharField("品番", max_length=4, default="0000")

       def __str__(self):
           return f"OrderedItem:{self.pk}:{self.code}:{self.name}"


   class PurchaseOrder(models.Model):
       """注文"""

       from_name = models.CharField("注文者名", max_length=50)
       ordered_at = models.DateTimeField("注文日時", auto_now_add=True)
       ordered_items = models.ManyToManyField(
           OrderedItem, verbose_name="発注に含まれる商品"
       )

       def __str__(self):
           return f"PurchaseOrder:{self.pk}:{self.from_name}"

shop/admin.py:

.. code-block:: python

   # ...
   admin.site.register(models.OrderedItem)
   admin.site.register(models.PurchaseOrder)

マイグレーション
~~~~~~~~~~~~~~~

.. code-block::

   (venv)$ python manage.py makemigrations shop
   (venv)$ python manage.py migrate

発注のフォームを作る
--------------------------------

Djangoにはモデルからフォームクラスを生成する機能があります。
今回はモデルに紐づく内容を入力するフォームなので、ModelFormを使うと簡単にフォームを作れます。

.. note::

   **Djangoのフォーム機能（django.forms）の役割**

   Djangoのフォーム機能には、次の機能があります。

   - Form
      - データの検証
      - Fieldを使ったデータの変換
      - フォーム用のHTMLタグの生成（Field.widget経由）
      - FormはFieldを内包する
   - Field
      - フィールド単位のデータの検証、変換
      - FieldはWidgetを内包する
   - Widget
      - Field単位のHTMLタグを生成する機能

ModelFormを使う
~~~~~~~~~~~~~~~~~~~~

shop/forms.py(新規作成):

.. code-block:: python

   from django import forms
   from .models import PurchaseOrder


   class OrderForm(forms.ModelForm):
       class Meta:
           model = PurchaseOrder
           fields = ["from_name"]

フォームを定義したら、Djangoのシェルで動作を見てみましょう。

.. code-block:: pycon

   (venv)$ python manage.py shell
   >>> from shop.forms import OrderForm
   >>> form = OrderForm()
   >>> print(form.as_p())
   <p>
       <label for="id_from_name">注文者名:</label>
       <input type="text" name="from_name" maxlength="50" required id="id_from_name">




     </p>
   >>> form2 = OrderForm({"from_name": "a" * 100})  # 50文字制限のところに100文字入れてみる
   >>> form2.is_valid()
   False
   >>> form2.errors
   {'from_name': ['この値は 50 文字以下でなければなりません( 100 文字になっています)。']}
   >>> print(form2.as_p())
   <ul class="errorlist"><li>この値は 50 文字以下でなければなりません( 100 文字になっています)。</li></ul>
     <p>
       <label for="id_from_name">注文者名:</label>
       <input type="text" name="from_name" value="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" maxlength="50" required aria-invalid="true" id="id_from_name">




     </p>
   >>> form3 = OrderForm({"from_name": "test"})
   >>> form3.save()  # ModelFormの場合、saveメソッドで Model.objects.create() が実行される
   <PurchaseOrder: PurchaseOrder:1:test>

発注のビュー
--------------------------------

shop/views.py:

.. code-block:: python

   # ...
   from .models import Item, OrderedItem, PurchaseOrder
   from . import forms

   # ...

   class OrderFormView(generic.CreateView):
       """注文フォーム"""

       model = PurchaseOrder
       form_class = forms.OrderForm
       success_url = reverse_lazy("order_complete")  # 保存後は完了画面へ

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

shop/urls.py:

.. code-block:: python

   # ...
   urlpatterns = [
       # ...
       path("order_form", views.OrderFormView.as_view(), name="order_form"),
   ]

shop/templates/shop/item_list.html:

.. code-block:: html+django

   {% block body %}
   # ...
   <br>
   <a href="{% url 'order_form' %}">注文へ進む</a>
   {% endblock %}

shop/templates/shop/purchaseorder_form.html(新規作成):

.. code-block:: html+django

   {% extends "base.html" %}

   {% block title %}注文フォーム{% endblock %}

   {% block body %}
   <h1>注文フォーム</h1>

   <form method="post">
   <div>
   {{ form.as_p }}
   </div>
   <div>
     <button type="submit">送信</button>
   </div>
   {% csrf_token %}
   </form>

   <h2>カート内の商品</h2>
   {% for cart_item in cart.items %}
   <div>{{ cart_item.name }} {{ cart_item.price }}円</div>
   {% endfor %}
   <a href="{% url 'clear_cart' %}">カートを空にする</a>
   {% endblock %}

動作確認の前に、完了画面の実装が必要です。一旦そのまま進めます。

完了画面
--------------------------------

注文フォームの保存が完了したときに表示するための完了画面を用意します。

shop/views.py:

.. code-block:: python

   # ...

   class OrderCompleteView(generic.TemplateView):
       template_name = "shop/complete.html"

shop/urls.py:

.. code-block:: python

   # ...

   urlpatterns = [
       # ...
       path("order_complete", views.OrderCompleteView.as_view(), name="order_complete"),
   ]

shop/templates/shop/complete.html(新規作成):

.. code-block:: html+django

   {% extends "base.html" %}

   {% block title %}注文完了{% endblock %}

   {% block body %}
   <h1>注文完了</h1>
   <p>
   注文が完了しました。
   </p>
   <a href="{% url 'item_list' %}">商品一覧にもどる</a>
   {% endblock %}

ここまで実装できたら動作確認をしてみましょう。

カートに商品を入れて、注文フォームに進み、フォームを送信して完了画面が表示されたら成功です。

クラスベースビューのフォーム生成機能を使う
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

クラスベースビューのCreateViewには、ModelFormを自動生成する処理が含まれています。

モデルに対応するフォームを使って保存するだけの場合は、CreateViewのフォーム生成機能を利用すると、フォームクラスの定義を省略できます。

shop/views.py:

.. code-block:: python

   # ...

   class OrderFormView(generic.CreateView):
       """注文フォーム"""

       model = PurchaseOrder
       # form_class = forms.OrderForm
       fields = ["from_name"]  # form_classの代わりにfieldsを定義する
       success_url = reverse_lazy("order_complete")

       # ...

自分で作成したOrderFormと動作は同じです。

ここまでで、ショッピングカートと注文フォームの実装は完了です。お疲れ様でした。

追加課題
--------------------------------

時間に余裕のある人向けの追加課題です。

- カート内の商品を個別に削除できるようにする
- 管理画面のPurchaseOrderの編集フォームで、ordered_itemsを見やすくする（StackedInlineを使ってみる）
- CartItemとOrderedItemで商品ごとの数量を保持できるように変更し、カートに同一商品を追加する場合は数量だけを増やす形にする
- カートに商品を追加する処理をPOSTメソッドに変更する
      - GETメソッドだと、外部サイトに貼られたリンクを踏むだけでも商品をカートに入れることができてしまいます。POSTメソッドにしてCSRF対策をしてみましょう。
      - 同様にカートの商品を削除する処理もPOSTにしてみるとよいでしょう。
      - formタグをうまく使うと、JavaScript無しでも実装できます。
- セッションエンジンをキャッシュに変更し、キャッシュバックエンドをRedisにする
