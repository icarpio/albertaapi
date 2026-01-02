from rest_framework import serializers
from .models import Pizza, Order, OrderItem

# Serializador de Pizza
class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['id', 'name', 'description', 'price']

# Serializador para cada pizza dentro del pedido
class OrderItemSerializer(serializers.ModelSerializer):
    pizza = serializers.PrimaryKeyRelatedField(queryset=Pizza.objects.all())

    class Meta:
        model = OrderItem
        fields = ['pizza', 'quantity']

# Serializador principal del pedido
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)  # Permite múltiples pizzas por pedido

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone', 'message', 'items', 'created_at', 'delivered']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
