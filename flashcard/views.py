from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Flashcard, Categoria, FlashcardDesafio, Desafio
from .forms import FlashcardForm, DesafioForm


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


@login_required(login_url='login')
def excluir_flashcard(request: HttpRequest, id_flashcard: int) -> HttpResponse:
    flashcard = get_object_or_404(Flashcard, id=id_flashcard, user=request.user)
    flashcard.delete()
    messages.warning(request, 'Flashcard excluído com sucesso')
    return redirect(to='novo_flashcard')


@login_required(login_url='login')
def iniciar_desafio(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = DesafioForm(request.POST, user=request.user)

        if form.is_valid():
            desafio = form.save(commit=False)
            desafio.user = request.user
            desafio.save()
            desafio.categoria.add(*form.cleaned_data['categoria'])

            flashcards = (
                Flashcard.objects.filter(user=request.user)
                .filter(dificuldade=form.cleaned_data['dificuldade'])
                .filter(categoria_id__in=form.cleaned_data['categoria'])
                .order_by("?")
            )
            flashcards = flashcards[: int(form.cleaned_data['quantidade_perguntas'])]

            for f in flashcards:
                flashcard_desafio = FlashcardDesafio(flashcard=f)
                flashcard_desafio.save()
                desafio.flashcards.add(flashcard_desafio)

            return redirect(to='desafio', id_desafio=desafio.id)
    else:
        form = DesafioForm(user=request.user)

    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES
    context = {
        'form': form,
        'categorias': categorias,
        'dificuldades': dificuldades
    }
    return render(request, 'iniciar_desafio.html', context)


@login_required(login_url='login')
def listar_desafios(request: HttpRequest) -> HttpResponse:
    desafios = Desafio.objects.filter(user=request.user)
    categorias = Categoria.objects.all()
    dificuldades = Flashcard.DIFICULDADE_CHOICES

    filtro_categoria = request.GET.get("categoria")
    filtro_dificuldade = request.GET.get("dificuldade")

    if filtro_categoria:
        desafios = desafios.filter(categoria=filtro_categoria)
    if filtro_dificuldade:
        desafios = desafios.filter(dificuldade=filtro_dificuldade)

    context = {
        'desafios': desafios,
        'categorias': categorias,
        'dificuldades': dificuldades
    }
    return render(request, 'listar_desafios.html', context)

