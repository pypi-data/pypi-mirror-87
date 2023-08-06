MMD IDPay
=========

mmdidpay is a Django app to create pay link by IDPay and Manage transaction and following up them

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "mmdidpay" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mmdidpay',
    ]

2. Include the mmdidpay URLconf in your project urls.py like this::

    path('mmdidpay/', include('mmdidpay.urls')),

3. Run ``python manage.py migrate`` to create the mmdtransaction models.

4. Visit http://127.0.0.1:8000/mmdidpay/ to participate in the mmdidpay.