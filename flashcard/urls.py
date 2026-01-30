from django.urls import path

from . import views

urlpatterns = [
    path('novo_flashcard/', views.novo_flashcard, name='novo_flashcard'),
    path('excluir_flashcard/<int:id_flashcard>/', views.excluir_flashcard, name='excluir_flashcard'),
]
