from rest_framework import serializers
from .models import Account, WithdrawalSlip, DepositSlip, TransactionRequest, SettingSlip

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
        model = TransactionRequest
        fields = '__all__'

class SettingSlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingSlip
        fields = '__all__'