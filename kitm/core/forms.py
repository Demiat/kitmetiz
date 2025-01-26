from django import forms

from .models import Nomenclature


class NomenclatureForm(forms.ModelForm):
    """Форма Номенклатуры"""
    
    class Meta:
        model = Nomenclature
