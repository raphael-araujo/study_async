from django import forms
from django.core.exceptions import ValidationError

from .models import Flashcard, Desafio


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['pergunta', 'resposta', 'categoria', 'dificuldade']


class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ['titulo', 'categoria', 'dificuldade', 'quantidade_perguntas']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        dificuldade = cleaned_data.get('dificuldade')
        categoria = cleaned_data.get('categoria')
        quantidade_perguntas = cleaned_data.get('quantidade_perguntas')

        if categoria and dificuldade and quantidade_perguntas and self.user:
            total_flashcards = (
                Flashcard.objects.filter(user=self.user)
                .filter(dificuldade=dificuldade)
                .filter(categoria_id__in=categoria)
            ).count()

            if quantidade_perguntas > total_flashcards:
                raise ValidationError({
                    'quantidade_perguntas': (
                        f"Você pediu {quantidade_perguntas} pergunta(s), "
                        f"mas existem {total_flashcards} flashcards disponíveis "
                        f"nessa categoria/dificuldade."
                    )
                })

        return cleaned_data
