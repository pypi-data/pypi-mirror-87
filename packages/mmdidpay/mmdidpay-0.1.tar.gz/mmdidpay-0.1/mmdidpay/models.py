import threading

from django.contrib.auth.models import User
from django.db import models
from mmdidpay.IDPay import IDPay
from django.conf import settings


class PayTransaction(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.SET_DEFAULT, default=None)
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=-1)
    track_id = models.IntegerField(default=-1)
    idpay_track_id = models.IntegerField(default=-1)
    pay_id = models.CharField(max_length=100)
    order_id = models.CharField(max_length=100)
    card_no = models.CharField(max_length=100)
    pay_date = models.CharField(max_length=100)
    received_response = models.BooleanField(default=False)
    success = models.BooleanField(default=False)
    link = models.CharField(max_length=100, null=False, blank=False)
    product_key = models.CharField(max_length=100, default='', blank=True, null=False)
    user_url_redirect = models.CharField(max_length=100, default='127.0.0.1:8000', blank=False, null=False)

    def on_success_buy(self):
        pass

    def update_state_with_response(self, response):
        self.status = int(response['status'])
        self.idpay_track_id = int(response['track_id'])
        self.track_id = response['track_id']
        self.pay_date = response['date']

        if response.__contains__('payment'):
            payment = response['payment']

            self.card_no = payment['card_no']
            self.track_id = payment['track_id']

        self.received_response = True

        if self.status == 100:
            self.success = True
            try:
                self.on_success_buy()
            except Exception as error:
                print(error)

        self.save()

        if self.status == 10:
            self.verify()

    def follow_up(self):
        response = self.__get_inquiry()
        self.update_state_with_response(response)

    def verify(self):
        id_pay = IDPay(api_key=settings.PAY_API_KEY, sandbox=False)
        response = id_pay.verify(id=self.pay_id, order_id=self.order_id)
        self.update_state_with_response(response)

    def __get_inquiry(self):
        id_pay = IDPay(api_key=settings.PAY_API_KEY, sandbox=False)
        response = id_pay.inquiry(id=self.pay_id, order_id=self.order_id)
        return response

    @staticmethod
    def create_new_transaction_link(product_key, price, user: User, sandbox=False):

        order_id = 'product' + product_key + '-username:' + str(user.username)

        id_pay = IDPay(api_key=settings.PAY_API_KEY, sandbox=sandbox)

        response = id_pay.new_transaction(order_id=order_id, amount=price, callback=settings.PAY_CALLBACK_URL)

        if response.__contains__('id'):
            pay_id = response['id']
            link = response['link']

            transaction = PayTransaction.objects.create(amount=price, order_id=order_id, product_key=product_key,
                                                        pay_id=pay_id, link=link, user=user)

            threading.Timer(9 * 60, transaction.follow_up).start()

            return link
        else:
            return Exception('Some errors in IDPay api\n' + str(response))
