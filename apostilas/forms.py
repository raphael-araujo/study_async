from django import forms

from apostilas.models import Apostila


class ApostilasForm(forms.ModelForm):
    class Meta:
        model = Apostila
        fields = ['titulo', 'arquivo']
