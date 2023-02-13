from django.urls import path
from .views import ItemView, APIBuyItemView, APIBuyOrderView, OrderView

urlpatterns = [
    path('item/<int:pk>', ItemView.as_view(), name='item'),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
    path('buy/<int:pk>', APIBuyItemView.as_view(), name='buy'),
    path('buy_order/<int:pk>', APIBuyOrderView.as_view(), name='buy_order'),
]