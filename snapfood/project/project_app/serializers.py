from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import CustomUser, Food, Order


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['food', 'user']
        depth = 1

    def to_representation(self, instance):
        data = super(OrderSerializer, self).to_representation(instance)
        return {
            'food':data['food'][0]['name'],
            'user':data['user']['name']

        }


class UserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(many=True, queryset=Order.objects.all())
    class Meta:
        model = CustomUser
        fields =['number', 'name', 'orders']
        extra_kwargs = {
            'orders': {
                'read_only': True
            }
        }


class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['number', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.object.create_user(validated_data['number'], validated_data['name'])
        user.set_password(validated_data['password'])
        user.save()

        return user


