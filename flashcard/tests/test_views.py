import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from flashcard.models import Categoria, Flashcard, FlashcardDesafio, Desafio


# ==============================================================================
# TESTES DE VIEWS - flashcard/views.py
# ==============================================================================

@pytest.mark.django_db
class TestNovoFlashcardView:

    @pytest.fixture
    def usuario_logado(self, client):
        user = User.objects.create_user(username="viewuser", password="senha123")
        client.login(username="viewuser", password="senha123")
        return user

    def test_redireciona_usuario_nao_autenticado(self, client):
        url = reverse("novo_flashcard")
        response = client.get(url)
        assert response.status_code == 302
        assert "/login" in response["Location"]

    def test_get_retorna_200_para_autenticado(self, client, usuario_logado):
        url = reverse("novo_flashcard")
        response = client.get(url)
        assert response.status_code == 200

    def test_post_flashcard_valido_cria_e_redireciona(self, client, usuario_logado):
        cat = Categoria.objects.create(nome="Teste")
        url = reverse("novo_flashcard")
        data = {
            "pergunta": "O que é Python?",
            "resposta": "Uma linguagem de programação.",
            "categoria": cat.id,
            "dificuldade": "F",
        }
        response = client.post(url, data)
        assert response.status_code == 302

    def test_filtro_por_categoria(self, client, usuario_logado):
        cat = Categoria.objects.create(nome="Backend")
        Flashcard.objects.create(
            user=usuario_logado, pergunta="P1", resposta="R1", categoria=cat, dificuldade="F"
        )
        url = reverse("novo_flashcard") + f"?categoria={cat.id}"
        response = client.get(url)
        assert response.status_code == 200

    def test_filtro_por_dificuldade(self, client, usuario_logado):
        cat = Categoria.objects.create(nome="Frontend")
        Flashcard.objects.create(
            user=usuario_logado, pergunta="P2", resposta="R2", categoria=cat, dificuldade="D"
        )
        url = reverse("novo_flashcard") + "?dificuldade=D"
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
class TestExcluirFlashcardView:

    @pytest.fixture
    def setup(self, client):
        user = User.objects.create_user(username="excluiruser", password="senha123")
        client.login(username="excluiruser", password="senha123")
        cat = Categoria.objects.create(nome="Cloud")
        fc = Flashcard.objects.create(
            user=user, pergunta="O que é AWS?", resposta="...", categoria=cat, dificuldade="M"
        )
        return user, fc

    def test_excluir_flashcard_proprio(self, client, setup):
        user, fc = setup
        url = reverse("excluir_flashcard", kwargs={"id_flashcard": fc.id})
        response = client.post(url)
        assert response.status_code == 302
        assert not Flashcard.objects.filter(id=fc.id).exists()

    def test_excluir_flashcard_de_outro_usuario_retorna_404(self, client):
        outro = User.objects.create_user(username="outro", password="senha123")
        cat = Categoria.objects.create(nome="DevOps")
        fc = Flashcard.objects.create(
            user=outro, pergunta="O que é Docker?", resposta="...", categoria=cat, dificuldade="D"
        )
        # Loga com um usuário diferente
        User.objects.create_user(username="intruso", password="senha123")
        client.login(username="intruso", password="senha123")
        url = reverse("excluir_flashcard", kwargs={"id_flashcard": fc.id})
        response = client.post(url)
        assert response.status_code == 404

    def test_excluir_flashcard_sem_autenticacao_redireciona(self, client):
        url = reverse("excluir_flashcard", kwargs={"id_flashcard": 999})
        response = client.post(url)
        assert response.status_code == 302
        assert "/login" in response["Location"]


@pytest.mark.django_db
class TestDesafioView:

    @pytest.fixture
    def setup(self, client):
        user = User.objects.create_user(username="desafiouser", password="senha123")
        client.login(username="desafiouser", password="senha123")
        cat = Categoria.objects.create(nome="Testes")
        desafio = Desafio.objects.create(
            user=user, titulo="Desafio Teste", quantidade_perguntas=3, dificuldade="F"
        )
        desafio.categoria.add(cat)
        return user, desafio

    def test_desafio_retorna_200_para_dono(self, client, setup):
        user, desafio = setup
        url = reverse("desafio", kwargs={"id_desafio": desafio.id})
        response = client.get(url)
        assert response.status_code == 200

    def test_desafio_retorna_403_para_outro_usuario(self, client, setup):
        _, desafio = setup
        User.objects.create_user(username="invasor", password="senha123")
        client.login(username="invasor", password="senha123")
        url = reverse("desafio", kwargs={"id_desafio": desafio.id})
        response = client.get(url)
        assert response.status_code == 403

    def test_desafio_retorna_404_para_id_inexistente(self, client, setup):
        url = reverse("desafio", kwargs={"id_desafio": 99999})
        response = client.get(url)
        assert response.status_code == 404

    def test_context_contagem_acertos_erros_faltantes(self, client, setup):
        user, desafio = setup
        cat = Categoria.objects.create(nome="Extra")
        fc = Flashcard.objects.create(
            user=user, pergunta="P?", resposta="R", categoria=cat, dificuldade="F"
        )
        fcd = FlashcardDesafio.objects.create(flashcard=fc, respondido=True, acertou=True)
        desafio.flashcards.add(fcd)

        url = reverse("desafio", kwargs={"id_desafio": desafio.id})
        response = client.get(url)
        assert response.context["acertos"] == 1
        assert response.context["erros"] == 0


@pytest.mark.django_db
class TestResponderFlashcardView:

    @pytest.fixture
    def setup(self, client):
        user = User.objects.create_user(username="responderuser", password="senha123")
        client.login(username="responderuser", password="senha123")
        cat = Categoria.objects.create(nome="API")
        fc = Flashcard.objects.create(
            user=user, pergunta="O que é REST?", resposta="...", categoria=cat, dificuldade="M"
        )
        fcd = FlashcardDesafio.objects.create(flashcard=fc)
        desafio = Desafio.objects.create(
            user=user, titulo="D", quantidade_perguntas=1, dificuldade="M"
        )
        desafio.flashcards.add(fcd)
        return user, fcd, desafio

    def test_responder_acertou(self, client, setup):
        user, fcd, desafio = setup
        url = reverse("responder_flashcard", kwargs={"id_flashcard": fcd.id})
        client.get(url, {"acertou": "1", "desafio_id": desafio.id})
        fcd.refresh_from_db()
        assert fcd.respondido is True
        assert fcd.acertou is True

    def test_responder_errou(self, client, setup):
        user, fcd, desafio = setup
        url = reverse("responder_flashcard", kwargs={"id_flashcard": fcd.id})
        client.get(url, {"acertou": "0", "desafio_id": desafio.id})
        fcd.refresh_from_db()
        assert fcd.respondido is True
        assert fcd.acertou is False

    def test_responder_flashcard_de_outro_usuario_retorna_403(self, client, setup):
        _, fcd, desafio = setup
        User.objects.create_user(username="invasor2", password="senha123")
        client.login(username="invasor2", password="senha123")
        url = reverse("responder_flashcard", kwargs={"id_flashcard": fcd.id})
        response = client.get(url, {"acertou": "1", "desafio_id": desafio.id})
        assert response.status_code == 403
