from django.contrib import auth, messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from usuarios.forms import CadastroForm


def cadastro(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)

            messages.success(request, "Usuário criado com sucesso.")
            return redirect(to="novo_flashcard")
    else:
        if request.user.is_authenticated:
            return redirect(to="novo_flashcard")
        form = CadastroForm()

    return render(request, "cadastro.html", {"form": form})
