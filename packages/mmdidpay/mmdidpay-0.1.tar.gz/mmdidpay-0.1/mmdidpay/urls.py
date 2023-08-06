from django.urls import path
from . import admin_views

urlpatterns = [
    # admin
    path('response/', admin_views.get_response, name='get-pay-response'),
    path('callback/', admin_views.get_response, name='get-pay-callback'),
    path('test/', admin_views.test_pay, name='test-pay'),
    path('delete-transaction/<int:transaction_id>/', admin_views.delete_transaction_id, name='delete-transaction'),
    path('follow_up_transaction/<int:pay_transaction_id>/', admin_views.follow_up_transaction, name='follow-up-transaction'),
    path('all/', admin_views.all_transactions, name='all-transactions'),
]
