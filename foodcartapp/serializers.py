from rest_framework.serializers import ModelSerializer, IntegerField
from .models import Order, OrderElement


class OrderElementSerializer(ModelSerializer):

    class Meta:
        model = OrderElement
        fields = ['quantity', 'product']

    def create(self, validated_data):
        return OrderElement.objects.create(**validated_data)


class OrderSerializer(ModelSerializer):
    id = IntegerField(read_only=True)
    products = OrderElementSerializer(
        many=True, allow_empty=False, write_only=True
    )

    class Meta:
        model = Order
        fields = [
            'id',
            'address',
            'firstname',
            'lastname',
            'phonenumber',
            'products'
        ]
