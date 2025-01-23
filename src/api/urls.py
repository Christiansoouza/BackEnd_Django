from django.urls import path
from .views import userView

urlpatterns = [
    path('api/user/', userView.as_view(), name='user-api'),
]