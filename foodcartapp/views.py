from pprint import pprint

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
import phonenumbers

from .models import Product, Order, OrderElement


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
    # order = json.loads(request.body.decode())
    order = request.data
    pprint(order)
    phonenumber = phonenumbers.parse(order.get('phonenumber'), 'RU')
    if phonenumbers.is_valid_number(phonenumber):
        valid_phonenumber = phonenumbers.format_number(
            phonenumber,
            phonenumbers.PhoneNumberFormat.E164
        )
    created_order = Order.objects.create(
        address=order.get('address'),
        firstname=order.get('firstname'),
        lastname=order.get('lastname'),
        phonenumber=valid_phonenumber,
    )
    all_products = Product.objects.all()
    for product in order.get('products'):
        OrderElement.objects.create(
            order=created_order,
            product=all_products.get(id=product.get('product')),
            quantity=product.get('quantity'),
        )
    return Response()
