from rest_framework import serializers
from .models import Account, WithdrawalSlip, DepositSlip, TransactionRequest

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class WithdrawalSlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawalSlip
        fields = '__all__'

class DepositSlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositSlip
        fields = '__all__'

class TransactionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositSlip
        fields = '__all__'