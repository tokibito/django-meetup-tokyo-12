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

サンプルコード
--------------

GitHub上にサンプルコードがあります。

https://github.com/tokibito/django-meetup-tokyo-12/

資料
----

https://tokibito.github.io/django-meetup-tokyo-12/

（準備中です）

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

今回は ``myproject`` という名前のプロジェクトで作成します。

.. code-block::

   (venv)$ django-admin startproject myproject

django-debug-toolbarをインストール、セットアップしておきます。

.. code-block::

   (venv)$ pip install django-debug-toolbar

.. note::

   - `django-debug-toolbar <https://django-debug-toolbar.readthedocs.io/en/latest/>`_
   - `はじめてのDjangoアプリ作成、その8 | Django ドキュメント <https://docs.djangoproject.com/ja/5.0/intro/tutorial08/>`_

.. toctree::
   :maxdepth: 2
