from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from apostilas.forms import ApostilasForm
from apostilas.models import Apostila, ViewApostila


@login_required(login_url='login')
def adicionar_apostilas(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ApostilasForm(request.POST, request.FILES)
        if form.is_valid():
            apostila = form.save(commit=False)
            apostila.user = request.user
            apostila.save()
            messages.success(request, 'Apostila adicionada com sucesso')

            return redirect(to='adicionar_apostilas')
    else:
        form = ApostilasForm()

    apostilas = Apostila.objects.filter(user=request.user)
    views_totais = ViewApostila.objects.filter(apostila__user=request.user).count()
    context = {
        'form': form,
        'apostilas': apostilas,
        'views_totais': views_totais,
    }
    return render(request, 'adicionar_apostilas.html', context)


@login_required(login_url='login')
def apostila(request: HttpRequest, id_apostila: int) -> HttpResponse:
    apostila = get_object_or_404(Apostila, id=id_apostila)
    view = ViewApostila.objects.create(
        ip=request.META['REMOTE_ADDR'],
        apostila=apostila
    )
    view.save()

    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    views_totais = ViewApostila.objects.filter(apostila=apostila).values('ip').count()

    context = {
        'apostila': apostila,
        'views_unicas': views_unicas,
        'views_totais': views_totais,
    }
    return render(request, 'apostila.html', context)
