from django.views.generic import DetailView
from django.shortcuts import redirect
from django.http import HttpRequest

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Item, Order

import stripe
import os

stripe.api_key = os.environ.get('STRIPE_TOKEN')


class ItemView(DetailView):
    model = Item
    template_name = 'main/item_detail.html'
    context_object_name = 'item'

class OrderView(DetailView):
    model = Order
    template_name = 'main/order_detail.html'
    context_object_name = 'order'

class APIBuyItemView(APIView):

    def get(self, request: HttpRequest, **kwargs) -> Response:
        host = request.get_host()
        scheme = request.scheme
        id = kwargs.get('pk')
        product_qs = Item.objects.filter(id=id)
        if product_qs.exists():
            product = product_qs.first()
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': product.currency,
                        'product_data': {
                            'name': product.name,
                        },
                        'unit_amount': product.price * 100,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'{scheme}://{host}/success',
                cancel_url=f'{scheme}://{host}/cancel',
            )
            return redirect(session.url, code=303)
        else:
            return Response(status=404)


class APIBuyOrderView(APIView):

    def get(self, request: Request, **kwargs):
        host = request.get_host()
        scheme = request.scheme
        id = kwargs.get('pk')
        order_qs = Order.objects.filter(id=id)
        if order_qs.exists():
            order = order_qs.first()
            """
            By logic one order MUST have only one discount or tax. 
            Preventing mistakes in logic can be resolved in Django Admin by customizing Discount admin class with limitation of QuerySet available Orders or, more easily change from fk to 1to1 relation.
            Tax the same.
            """
            discount_qs = order.discount_order
            # tax_qs = order.tax_order

            if discount_qs.exists():
                discount = discount_qs.first().as_dict()
            else:
                discount = {}

            # if tax_qs.exists():
            #     tax = tax_qs.first().as_dict()
            # else:
            #     tax = {}
            session = stripe.checkout.Session.create(
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': order,
                            'description': ', '.join([item.name for item in order.items.all()])
                        },
                        'unit_amount': order.total(),
                    },
                    'quantity': 1,
                    # 'tax_rates': tax was not implemented.
                }],
                mode='payment',
                success_url=f'{scheme}://{host}/success',
                cancel_url=f'{scheme}://{host}/cancel',
                discounts=discount
            )
            return redirect(session.url, code=303)
        else:
            return Response(status=404)