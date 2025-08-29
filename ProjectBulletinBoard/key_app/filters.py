from django.forms import DateInput
from django_filters import FilterSet, CharFilter, MultipleChoiceFilter


class ReplyFilter(FilterSet):
    advertisement_title = CharFilter(field_name='advertisement__title', lookup_expr='exact', label='Объявление')
    is_accepted = MultipleChoiceFilter(field_name='is_accepted', choices=[(True, "Принят"), (False, "Не принят")],
                                       label='Статус')
    create_datetime = CharFilter(field_name='create_datetime', lookup_expr='gt',
                                 widget=DateInput(attrs={'type': 'date'}), label='Созданы позже')
    last_change_datetime = CharFilter(field_name='last_change_datetime', lookup_expr='gt',
                                      widget=DateInput(attrs={'type': 'date'}),
                                      label='Изменены позже')
    user_username = CharFilter(field_name='user__username', lookup_expr='exact', label='Пользователь')
