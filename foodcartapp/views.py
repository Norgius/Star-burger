from pprint import pprint

from django.http import JsonResponse
from django.templatetags.static import static
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import phonenumbers

from .models import Product, Order, OrderElement


def check_order_keys(raw_order):
    order_keys = ('address', 'firstname', 'lastname', 'phonenumber')
    missing_keys = []
    raw_products = raw_order.get('products')
    if not raw_products or not isinstance(raw_products, list):
        return {'error': 'products key not presented or not list'}
    for order_key in order_keys:
        raw_order_key = raw_order.get(order_key)
        if not raw_order_key or not isinstance(raw_order_key, str):
            missing_keys.append(order_key)
    if missing_keys:
        return {'error': f'The keys {missing_keys} not specified or not str'}


def check_valid_phonenumber(raw_phonenumber):
    phonenumber = phonenumbers.parse(raw_phonenumber, 'RU')
    error_content = None
    if not phonenumbers.is_valid_number(phonenumber):
        error_content = {
            'error': f'Such phonenumber={raw_phonenumber} does not exist'
        }
    valid_phonenumber = phonenumbers.format_number(
        phonenumber,
        phonenumbers.PhoneNumberFormat.E164,
    )
    return valid_phonenumber, error_content


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@api_view(['POST'])
def register_order(request):
    raw_order = request.data
    pprint(raw_order)
    error_content = check_order_keys(raw_order)
    if error_content:
        return Response(error_content, status=status.HTTP_204_NO_CONTENT)
    valid_phonenumber, error_content = check_valid_phonenumber(
        raw_order.get('phonenumber'))
    if error_content:
        return Response(error_content, status=status.HTTP_204_NO_CONTENT)
    all_products = Product.objects.all()
    for product in raw_order.get('products'):
        if not all_products.filter(id=product.get('product')).exists():
            error_content = {'error': 'Such product id does not exist'}
            return Response(error_content, status=status.HTTP_404_NOT_FOUND)

    created_order = Order.objects.create(
        address=raw_order.get('address'),
        firstname=raw_order.get('firstname'),
        lastname=raw_order.get('lastname'),
        phonenumber=valid_phonenumber,
    )

    for product in raw_order.get('products'):
        OrderElement.objects.create(
            order=created_order,
            product=all_products.get(id=product.get('product')),
            quantity=product.get('quantity'),
        )
    return Response()
