import json
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from mmdidpay.models import PayTransaction


@csrf_exempt
def get_response(request):
    pay_id = request.POST.get('id')
    order_id = request.POST.get('order_id')

    transaction = PayTransaction.objects.filter(pay_id=pay_id, order_id=order_id)
    if not transaction.exists():
        raise Http404
    transaction = transaction.get()

    transaction.update_state_with_response(request.POST)

    return redirect(transaction.user_url_redirect)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def test_pay(request):
    user = User.objects.first()

    try:
        link = PayTransaction.create_new_transaction_link(user=user, price=1000, product_key='Pay test', sandbox=True)
    except Exception as e:
        return HttpResponse(str(e))

    return HttpResponseRedirect(link)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def follow_up_transaction(request, pay_transaction_id):
    transaction = PayTransaction.objects.get(id=pay_transaction_id)
    transaction.follow_up()
    return redirect('all-transactions')


@user_passes_test(lambda u: u.is_superuser)
@login_required
def all_transactions(request):
    data = {'transactions': PayTransaction.objects.all()}
    return render(request, 'transactions.html', data)


@user_passes_test(lambda u: u.is_superuser)
@login_required
def delete_transaction_id(request, transaction_id):
    PayTransaction.objects.filter(id=transaction_id).delete()
    return redirect('all-transactions')
