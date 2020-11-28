from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import CustomUser, Food, Order
from .serializers import FoodSerializer, OrderSerializer, UserSerializer, SingUpSerializer
from .permissions import IsOrder, IsAdmin
from django.shortcuts import Http404
from django.shortcuts import get_object_or_404
from .filters import ContactFilter
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

class FoodViewSet(viewsets.ViewSet):
    permission_classes = (IsAdmin, )
    serializer_class = FoodSerializer
    queryset = Food.objects.all()


    def get_object(self, pk):
        try:
            return Food.objects.get(pk=pk)
        except Food.DoesNotExist:
            raise Http404

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = self.get_object(pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object(pk)
        instance.delete()
        instance.save()
        return Response(data='delete success')


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsOrder)
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user.is_staff
        if user==True:
            print(Order.objects.all())
            return Order.objects.all()
        else:
            user = self.request.user
            return Order.objects.filter(user=user)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserView(generics.ListAPIView):
    queryset = CustomUser.object.all()
    serializer_class = UserSerializer
    filter_class = ContactFilter
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['^name']

class SignUpUserView(generics.CreateAPIView):
    serializer_class = SingUpSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        number = request.data['number']
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
