from django import forms

from .models import Flashcard, Desafio


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['pergunta', 'resposta', 'categoria', 'dificuldade']


class DesafioForm(forms.ModelForm):
    class Meta:
        model = Desafio
        fields = ['titulo', 'categoria', 'dificuldade', 'quantidade_perguntas']
