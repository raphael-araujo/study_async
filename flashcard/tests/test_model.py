import pytest
from django.contrib.auth.models import User

from flashcard.models import Categoria, Flashcard, FlashcardDesafio, Desafio


# ==============================================================================
# TESTES DE MODELS - flashcard/models.py
# ==============================================================================

@pytest.mark.django_db
class TestCategoriaModel:

    def test_criacao_categoria(self):
        categoria = Categoria.objects.create(nome="Python")
        assert categoria.nome == "Python"

    def test_str_categoria(self):
        categoria = Categoria(nome="Django")
        assert str(categoria) == "Django"

    def test_nome_max_length(self):
        field = Categoria._meta.get_field("nome")
        assert field.max_length == 20


@pytest.mark.django_db
class TestFlashcardModel:

    @pytest.fixture
    def usuario(self):
        return User.objects.create_user(username="testuser", password="senha123")

    @pytest.fixture
    def categoria(self):
        return Categoria.objects.create(nome="Python")

    def test_criacao_flashcard(self, usuario, categoria):
        fc = Flashcard.objects.create(
            user=usuario,
            pergunta="O que é Django?",
            resposta="Um framework web Python.",
            categoria=categoria,
            dificuldade="F",
        )
        assert fc.pergunta == "O que é Django?"
        assert fc.resposta == "Um framework web Python."
        assert fc.dificuldade == "F"

    def test_str_flashcard(self, usuario, categoria):
        fc = Flashcard(
            user=usuario,
            pergunta="O que é uma ORM?",
            resposta="...",
            categoria=categoria,
            dificuldade="M",
        )
        assert str(fc) == "O que é uma ORM?"

    def test_css_dificuldade_facil(self, usuario, categoria):
        fc = Flashcard(user=usuario, pergunta="P", resposta="R", categoria=categoria, dificuldade="F")
        assert fc.css_dificuldade == "flashcard-facil"

    def test_css_dificuldade_medio(self, usuario, categoria):
        fc = Flashcard(user=usuario, pergunta="P", resposta="R", categoria=categoria, dificuldade="M")
        assert fc.css_dificuldade == "flashcard-medio"

    def test_css_dificuldade_dificil(self, usuario, categoria):
        fc = Flashcard(user=usuario, pergunta="P", resposta="R", categoria=categoria, dificuldade="D")
        assert fc.css_dificuldade == "flashcard-dificil"

    def test_css_dificuldade_valor_invalido(self, usuario, categoria):
        fc = Flashcard(user=usuario, pergunta="P", resposta="R", categoria=categoria, dificuldade="X")
        assert fc.css_dificuldade is None

    def test_dificuldade_choices(self):
        choices = dict(Flashcard.DIFICULDADE_CHOICES)
        assert choices["F"] == "Fácil"
        assert choices["M"] == "Médio"
        assert choices["D"] == "Difícil"


@pytest.mark.django_db
class TestFlashcardDesafioModel:

    @pytest.fixture
    def flashcard(self):
        user = User.objects.create_user(username="u1", password="pass")
        cat = Categoria.objects.create(nome="SQL")
        return Flashcard.objects.create(
            user=user, pergunta="O que é JOIN?", resposta="...", categoria=cat, dificuldade="M"
        )

    def test_criacao_flashcard_desafio(self, flashcard):
        fcd = FlashcardDesafio.objects.create(flashcard=flashcard)
        assert fcd.respondido is False
        assert fcd.acertou is False

    def test_str_flashcard_desafio(self, flashcard):
        fcd = FlashcardDesafio(flashcard=flashcard)
        assert str(fcd) == flashcard.pergunta

    def test_marcar_como_respondido_e_acertou(self, flashcard):
        fcd = FlashcardDesafio.objects.create(flashcard=flashcard, respondido=True, acertou=True)
        assert fcd.respondido is True
        assert fcd.acertou is True


@pytest.mark.django_db
class TestDesafioModel:

    @pytest.fixture
    def setup(self):
        user = User.objects.create_user(username="u2", password="pass")
        cat = Categoria.objects.create(nome="Git")
        return user, cat

    def test_criacao_desafio(self, setup):
        user, cat = setup
        desafio = Desafio.objects.create(
            user=user, titulo="Desafio Python", quantidade_perguntas=5, dificuldade="F"
        )
        desafio.categoria.add(cat)
        assert desafio.titulo == "Desafio Python"
        assert desafio.quantidade_perguntas == 5

    def test_str_desafio(self, setup):
        user, _ = setup
        desafio = Desafio(user=user, titulo="Meu Desafio", quantidade_perguntas=3, dificuldade="D")
        assert str(desafio) == "Meu Desafio"

    def test_desafio_relacionamento_categoria(self, setup):
        user, cat = setup
        desafio = Desafio.objects.create(
            user=user, titulo="Desafio Cat", quantidade_perguntas=2, dificuldade="M"
        )
        desafio.categoria.add(cat)
        assert cat in desafio.categoria.all()
