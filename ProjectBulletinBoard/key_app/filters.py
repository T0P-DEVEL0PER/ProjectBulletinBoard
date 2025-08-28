from django.forms import DateInput
from django_filters import FilterSet, CharFilter

from .models import Reply


class ReplyFilter(FilterSet):
    create_datetime = CharFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))
    last_change_datetime = CharFilter(lookup_expr='gt', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Reply
        fields = {'advertisement': ['exact'],
            'text': ['exact'],
            'is_accepted': ['exact'],
            'user': ['exact'],
        }
