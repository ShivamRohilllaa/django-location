from django.urls import path
from .views import CustomerListCreateView, CustomerDetailView, UserLoginView

urlpatterns = [
    path('customers/', CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('login/', UserLoginView.as_view(), name='user-login'),
]