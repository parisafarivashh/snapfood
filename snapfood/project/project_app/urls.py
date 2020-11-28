from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodViewSet, OrderViewSet, UserView, SignUpUserView


router = DefaultRouter()
router.register('food', FoodViewSet)
router.register('order', OrderViewSet, basename='order')

urlpatterns = [
    path('api/', include(router.urls)),
    path('user/', UserView.as_view()),
    path('', SignUpUserView.as_view()),

]
