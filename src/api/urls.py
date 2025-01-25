from django.urls import path
from .views import UserView

urlpatterns = [
    path('api/user/', UserView.as_view(), name='user-api'),
]