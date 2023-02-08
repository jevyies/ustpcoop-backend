from django.shortcuts import render
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
import base64
import datetime
from deepface import DeepFace
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Value, CharField
from django.core.mail import send_mail
from django.conf import settings


from .serializer import AccountSerializer, WithdrawalSlipSerializer, DepositSlipSerializer, TransactionRequestSerializer
from .models import Account, WithdrawalSlip, DepositSlip, TransactionRequest


# for Account
class AccountList(APIView):
    def get(self, request, format=None):
        snippets = Account.objects.all()
        serializer = AccountSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if(request.data.get('purpose') == 'register'):
            serializer = AccountSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                with open("media/member-"+ str(account.id) +".jpg", "wb") as fh:
                    fh.write(base64.b64decode(request.data.get('image')))
                account.image_path = "media/member-"+ str(account.id) +".jpg"
                account.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif(request.data.get('purpose') == 'login'):
            try:
                account = Account.objects.get(email=request.data.get('email'), account_type=request.data.get('type'))
                if(account.account_no == ''):
                    return Response({'not_yet_valid': True}, status=status.HTTP_200_OK)
                else:
                    if(account.password == request.data.get('password')):
                        serializer = AccountSerializer(account)
                        return Response(serializer.data)
                    else:
                        return Response(status=status.HTTP_401_UNAUTHORIZED)
            except Account.DoesNotExist:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        elif(request.data.get('purpose') == 'change_status'):
            snippet = Account.objects.get(id=request.data.get('id'))
            serializer = AccountSerializer(snippet, data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                account.account_no = datetime.date.today().strftime("%Y%m") + '-' + str(snippet.id).rjust(6, '0')
                account.date_approved = datetime.date.today()
                account.save()
                if(account.account_status == 'approved'):
                    try:
                        send_mail(
                            'Account Approved',
                            'Your account has been approved. You can now login to your account.',
                            settings.EMAIL_HOST_USER,
                            [account.email],
                            fail_silently=False,
                        )
                    except Exception as e:
                        print(e)
                        return Response({'success': False, 'message': 'No connection could be made because the target machine actively refused it'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({'success': True, 'message': 'Successfully '+request.data.get('account_status')}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif(request.data.get('purpose') == 'update_details'):
            snippet = Account.objects.get(id=request.data.get('id'))
            serializer = AccountSerializer(snippet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': True, 'message': 'Successfully updated'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif(request.data.get('purpose') == 'update_password'):
            snippet = Account.objects.get(id=request.data.get('id'))
            if(snippet.password == request.data.get('old')):
                serializer = AccountSerializer(snippet, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'success': True, 'message': 'Successfully updated'}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success': False, 'message': 'Old password is incorrect'}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountDetail(APIView):
    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = AccountSerializer(snippet)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response({'success': True, 'message': 'Successfully deleted'}, status=status.HTTP_200_OK)

class AccountSearch(APIView):
    def get(self, request, format=None):
        if(len(request.query_params) == 0):
            snippets = Account.objects.all()
            serializer = AccountSerializer(snippets, many=True)
            return Response(serializer.data)
        else:
            if(request.query_params.get('account_status')):
                account = Account.objects.filter(account_status=request.query_params.get('account_status'), account_type='member')
                serializer = AccountSerializer(account, many=True)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

# for Withdrawal
class WithdrawalSlipList(APIView):
    def get(self, request, format=None):
        snippets = WithdrawalSlip.objects.all()
        serializer = WithdrawalSlipSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if(request.data.get('purpose') == 'request_withdrawal'):
            with open("media/account-withdrawal-"+ str(request.data.get('account')) +".jpg", "wb") as fh:
                fh.write(base64.b64decode(request.data.get('image')))
            # keras_models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "Dlib", "ArcFace"]
            # model_name = "DeepID"
            # model = DeepFace.build_model(model_name)
            try:
                result = DeepFace.verify("media/account-withdrawal-"+ str(request.data.get('account')) +".jpg", "media/member-"+ str(request.data.get('account')) +".jpg", model_name="DeepID")
                if(result['verified'] == False):
                    return Response({'success': False, 'message': 'Face Verification Failed'}, status=status.HTTP_200_OK)
                else:
                    serializer = WithdrawalSlipSerializer(data=request.data)
                    if serializer.is_valid():
                        withdrawal = serializer.save()
                        with open("media/withdrawal-"+ str(withdrawal.id) +".jpg", "wb") as fh:
                            fh.write(base64.b64decode(request.data.get('image')))
                        withdrawal.image_path_passed = "media/withdrawal-"+ str(withdrawal.id) +".jpg"
                        withdrawal.save()
                        return Response({'success': True, 'data' : serializer.data}, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(e)
                return Response({'success': False, 'message': 'Deep Face error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif(request.data.get('purpose') == 'change_status'):
            snippet = WithdrawalSlip.objects.get(id=request.data.get('id'))
            serializer = WithdrawalSlipSerializer(snippet, data=request.data)
            if serializer.is_valid():
                withdraw = serializer.save()
                withdraw.date_approved = datetime.date.today()
                withdraw.save()
                return Response({'success': True, 'message': 'Successfully '+request.data.get('status')}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class WithdrawalSlipDetail(APIView):
    def get_object(self, pk):
        try:
            return WithdrawalSlip.objects.get(pk=pk)
        except WithdrawalSlip.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = WithdrawalSlipSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = WithdrawalSlipSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# for Deposit
class UploadFileView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, format=None):
        file_obj = request.data['file']

class DepositSlipList(APIView):
    def get(self, request, format=None):
        snippets = DepositSlip.objects.all()
        serializer = DepositSlipSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if(request.data.get('purpose') == 'request_deposit'):
            serializer = DepositSlipSerializer(data=request.data)
            if serializer.is_valid():
                deposit = serializer.save()
                with open("media/deposit-"+ str(deposit.id) +".jpg", "wb") as fh:
                    fh.write(base64.b64decode(request.data.get('image')))
                deposit.image_path_passed = "media/deposit-"+ str(deposit.id) +".jpg"
                deposit.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif(request.data.get('purpose') == 'change_status'):
            snippet = DepositSlip.objects.get(id=request.data.get('id'))
            serializer = DepositSlipSerializer(snippet, data=request.data)
            if serializer.is_valid():
                deposit = serializer.save()
                deposit.date_approved = datetime.date.today()
                deposit.save()
                return Response({'success': True, 'message': 'Successfully '+request.data.get('status')}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class DepositSlipDetail(APIView):
    def get_object(self, pk):
        try:
            return DepositSlip.objects.get(pk=pk)
        except DepositSlip.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DepositSlipSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DepositSlipSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# for Transaction
class TransactionRequestList(APIView):
    def get(self, request, format=None):
        if(len(request.query_params) == 0):
            snippets = TransactionRequest.objects.all()
            serializer = TransactionRequestSerializer(snippets, many=True)
            return Response(serializer.data)
        else:
            if(request.query_params.get('purpose') == 'unite_transaction'):
                qs1 = DepositSlip.objects.select_related('account').filter(date_requested__range=(request.query_params.get('from'), request.query_params.get('to'))).values('id', 'account__name', 'account__account_no', 'account', 'date_requested', 'total_amount', 'image_path_passed', 'status').annotate(transaction_type=Value('deposit', CharField()))
                qs2 = WithdrawalSlip.objects.select_related('account').filter(date_requested__range=(request.query_params.get('from'), request.query_params.get('to'))).values('id', 'account__name', 'account__account_no', 'account', 'date_requested', 'total_amount', 'image_path_passed', 'status').annotate(transaction_type=Value('withdrawal', CharField()))
                snippet = qs1.union(qs2, all=True).order_by('-date_requested')
                return Response(snippet)
            elif(request.query_params.get('purpose') == 'get_transaction_by_user'):
                qs1 = DepositSlip.objects.filter(status='approved', account=request.query_params.get('id'), date_requested__range=(request.query_params.get('from'), request.query_params.get('to'))).values('date_requested', 'total_amount', 'date_approved', 'status').annotate(transaction_type=Value('deposit', CharField()))
                qs2 = WithdrawalSlip.objects.filter(status='approved', account=request.query_params.get('id'), date_requested__range=(request.query_params.get('from'), request.query_params.get('to'))).values('date_requested', 'total_amount', 'date_approved', 'status').annotate(transaction_type=Value('withdrawal', CharField()))
                snippet = qs1.union(qs2, all=True).order_by('-date_requested')
                return Response(snippet)
            elif(request.query_params.get('purpose') == 'get_my_transaction'):
                qs1 = DepositSlip.objects.filter(account=request.query_params.get('id'), date_requested__range=(request.query_params.get('from'), request.query_params.get('to'))).values('date_requested', 'total_amount', 'date_approved', 'status').annotate(transaction_type=Value('deposit', CharField()))
                qs2 = WithdrawalSlip.objects.filter(account=request.query_params.get('id'), date_requested__range=(request.query_params.get('from'), request.query_params.get('to'))).values('date_requested', 'total_amount', 'date_approved', 'status').annotate(transaction_type=Value('withdrawal', CharField()))
                snippet = qs1.union(qs2, all=True).order_by('-date_requested')
                return Response(snippet)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        serializer = TransactionRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionRequestDetail(APIView):
    def get_object(self, pk):
        try:
            return TransactionRequest.objects.get(pk=pk)
        except TransactionRequest.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TransactionRequestSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TransactionRequestSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)