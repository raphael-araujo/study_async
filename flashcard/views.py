from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .forms import FlashcardForm
from .models import Flashcard, Categoria


@login_required(login_url='login')
def novo_flashcard(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcards = form.save(commit=False)
            flashcards.user = request.user
            flashcards.save()
            messages.success(request, 'Flashcard criado com sucesso')
            return redirect(to='novo_flashcard')

    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    form = FlashcardForm()

    filtro_categoria = request.GET.get("categoria")
    filtro_dificuldade = request.GET.get("dificuldade")
    flashcards = Flashcard.objects.filter(user=request.user).order_by("categoria")

    if filtro_categoria:
        flashcards = flashcards.filter(categoria=filtro_categoria)
    if filtro_dificuldade:
        flashcards = flashcards.filter(dificuldade=filtro_dificuldade)

    context = {
        'categorias': categorias,
        'dificuldades': dificuldades,
        'form': form,
        'flashcards': flashcards,
    }
    return render(request, 'novo_flashcard.html', context)
