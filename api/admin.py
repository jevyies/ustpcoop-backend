from django.contrib import admin
from . models import Account, WithdrawalSlip, DepositSlip, TransactionRequest
# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_no', 'name', 'email', 'password', 'image_path', 'date_registered', 'date_approved', 'account_type', 'account_status')
class WithdrawalSlipAdmin(admin.ModelAdmin):
    list_display = ('account', 'date_requested', 'total_amount', 'image_path_passed', 'status', 'date_approved')
class DepositSlipAdmin(admin.ModelAdmin):
    list_display = ('account', 'date_requested', 'total_amount', 'image_path_passed', 'status', 'date_approved')
class TransactionRequestAdmin(admin.ModelAdmin):
    list_display = ('account', 'request_remarks', 'date_requested', 'gcash')

admin.site.register(Account, AccountAdmin)
admin.site.register(WithdrawalSlip, WithdrawalSlipAdmin)
admin.site.register(DepositSlip, DepositSlipAdmin)
admin.site.register(TransactionRequest, TransactionRequestAdmin)