from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *


class AdvertisementForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок')
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория',
                                      empty_label="Выберите категорию")
    content = forms.CharField(widget=CKEditorWidget, label='Содержимое')

    class Meta:
        model = Advertisement
        fields = ['category']
