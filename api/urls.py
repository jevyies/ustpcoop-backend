from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
import api.views as views

urlpatterns = [
    path('api/', views.AccountList.as_view()),
    path('api/<int:pk>/', views.AccountDetail.as_view()),
    path('api-search/', views.AccountSearch.as_view()),
    path('deposit/', views.DepositSlipList.as_view()),
    path('deposit/<int:pk>/', views.DepositSlipDetail.as_view()),
    path('withdrawal/', views.WithdrawalSlipList.as_view()),
    path('withdrawal/<int:pk>/', views.WithdrawalSlipDetail.as_view()),
    path('transaction/', views.TransactionRequestList.as_view()),
    path('transaction/<int:pk>/', views.TransactionRequestDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)