from rest_framework import filters
import django_filters
from .models import CustomUser

class ContactFilter(django_filters.FilterSet):
   class Meta:
        model = CustomUser
        fields = {
            'name': ['startswith'],
            'number': ['startswith'],
        }
        together = ['name', 'number']


# class CustomSearchFilter(filters.SearchFilter):
#     def get_search_fields(self, view, request):
#         if request.get_queryset.get('name'):
#             return ['name']
#         return super(CustomSearchFilter, self).get_search_fields(view, request)

# class IsOwnFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         return queryset.filter(user=request.user)