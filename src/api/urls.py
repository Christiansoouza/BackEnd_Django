from django.urls import path
from .views import UserView, TransactionView

urlpatterns = [
    path('api/user/', UserView.as_view(), name='user-api'),
    path('api/transaction',TransactionView,name = 'transaction-api')
]   