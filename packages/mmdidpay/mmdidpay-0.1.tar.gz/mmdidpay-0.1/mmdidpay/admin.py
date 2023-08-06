from django.contrib import admin

# Register your models here.
from mmdidpay.models import PayTransaction


@admin.register(PayTransaction)
class TransactionAdmin(admin.ModelAdmin):
    pass
