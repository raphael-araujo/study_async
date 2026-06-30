import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apostilas.models import Apostila, ViewApostila


# ==============================================================================
# TESTES DE VIEWS - apostilas/views.py
# ==============================================================================

@pytest.mark.django_db
class TestAdicionarApostilasView:

    @pytest.fixture
    def usuario_logado(self, client):
        user = User.objects.create_user(username="addapostilauser", password="senha123")
        client.login(username="addapostilauser", password="senha123")
        return user

    def test_redireciona_usuario_nao_autenticado(self, client):
        url = reverse("adicionar_apostilas")
        response = client.get(url)
        assert response.status_code == 302
        assert "/login" in response["Location"]

    def test_get_retorna_200_para_autenticado(self, client, usuario_logado):
        url = reverse("adicionar_apostilas")
        response = client.get(url)
        assert response.status_code == 200

    def test_context_contem_form_apostilas_e_views_totais(self, client, usuario_logado):
        url = reverse("adicionar_apostilas")
        response = client.get(url)
        assert "form" in response.context
        assert "apostilas" in response.context
        assert "views_totais" in response.context

    def test_apostilas_no_context_apenas_do_usuario_logado(self, client, usuario_logado):
        outro = User.objects.create_user(username="outro", password="senha123")
        arquivo1 = SimpleUploadedFile("a1.pdf", b"pdf1", content_type="application/pdf")
        arquivo2 = SimpleUploadedFile("a2.pdf", b"pdf2", content_type="application/pdf")
        Apostila.objects.create(user=usuario_logado, titulo="Minha Apostila", arquivo=arquivo1)
        Apostila.objects.create(user=outro, titulo="Apostila Alheia", arquivo=arquivo2)

        url = reverse("adicionar_apostilas")
        response = client.get(url)
        apostilas = response.context["apostilas"]
        assert all(a.user == usuario_logado for a in apostilas)
        assert apostilas.count() == 1

    def test_post_valido_cria_apostila_e_redireciona(self, client, usuario_logado):
        url = reverse("adicionar_apostilas")
        arquivo = SimpleUploadedFile("nova.pdf", b"conteudo", content_type="application/pdf")
        data = {"titulo": "Nova Apostila", "arquivo": arquivo}
        response = client.post(url, data)
        assert response.status_code == 302
        assert Apostila.objects.filter(user=usuario_logado, titulo="Nova Apostila").exists()

    def test_post_invalido_nao_cria_apostila(self, client, usuario_logado):
        url = reverse("adicionar_apostilas")
        # POST sem arquivo (campo obrigatório)
        data = {"titulo": "Sem Arquivo"}
        response = client.post(url, data)
        assert response.status_code == 200  # Re-renderiza com erros
        assert not Apostila.objects.filter(titulo="Sem Arquivo").exists()

    def test_views_totais_contabiliza_corretamente(self, client, usuario_logado):
        arquivo = SimpleUploadedFile("b.pdf", b"pdf", content_type="application/pdf")
        apostila = Apostila.objects.create(user=usuario_logado, titulo="Apostila B", arquivo=arquivo)
        ViewApostila.objects.create(ip="1.1.1.1", apostila=apostila)
        ViewApostila.objects.create(ip="2.2.2.2", apostila=apostila)

        url = reverse("adicionar_apostilas")
        response = client.get(url)
        assert response.context["views_totais"] == 2

    def test_views_totais_nao_conta_apostilas_de_outro_usuario(self, client, usuario_logado):
        outro = User.objects.create_user(username="outro2", password="senha123")
        arquivo = SimpleUploadedFile("c.pdf", b"pdf", content_type="application/pdf")
        apostila_outro = Apostila.objects.create(user=outro, titulo="Alheia", arquivo=arquivo)
        ViewApostila.objects.create(ip="3.3.3.3", apostila=apostila_outro)

        url = reverse("adicionar_apostilas")
        response = client.get(url)
        assert response.context["views_totais"] == 0


@pytest.mark.django_db
class TestApostilaView:

    @pytest.fixture
    def setup(self, client):
        user = User.objects.create_user(username="apostilaviewuser", password="senha123")
        client.login(username="apostilaviewuser", password="senha123")
        arquivo = SimpleUploadedFile("teste.pdf", b"conteudo", content_type="application/pdf")
        apostila = Apostila.objects.create(user=user, titulo="Apostila View Test", arquivo=arquivo)
        return user, apostila

    def test_redireciona_usuario_nao_autenticado(self, client, setup):
        _, apostila = setup
        client.logout()
        url = reverse("apostila", kwargs={"id_apostila": apostila.id})
        response = client.get(url)
        assert response.status_code == 302
        assert "/login" in response["Location"]

    def test_get_retorna_200(self, client, setup):
        _, apostila = setup
        url = reverse("apostila", kwargs={"id_apostila": apostila.id})
        response = client.get(url)
        assert response.status_code == 200

    def test_get_retorna_404_para_id_inexistente(self, client, setup):
        url = reverse("apostila", kwargs={"id_apostila": 99999})
        response = client.get(url)
        assert response.status_code == 404

    def test_acesso_registra_view(self, client, setup):
        _, apostila = setup
        url = reverse("apostila", kwargs={"id_apostila": apostila.id})
        client.get(url)
        assert ViewApostila.objects.filter(apostila=apostila).count() == 1

    def test_acesso_multiplo_registra_multiplas_views(self, client, setup):
        _, apostila = setup
        url = reverse("apostila", kwargs={"id_apostila": apostila.id})
        client.get(url)
        client.get(url)
        assert ViewApostila.objects.filter(apostila=apostila).count() == 2

    def test_context_contem_apostila_views_unicas_e_totais(self, client, setup):
        _, apostila = setup
        url = reverse("apostila", kwargs={"id_apostila": apostila.id})
        response = client.get(url)
        assert "apostila" in response.context
        assert "views_unicas" in response.context
        assert "views_totais" in response.context

    def test_context_apostila_correta(self, client, setup):
        _, apostila = setup
        url = reverse("apostila", kwargs={"id_apostila": apostila.id})
        response = client.get(url)
        assert response.context["apostila"] == apostila

    def test_views_totais_incrementa_a_cada_acesso(self, client, setup):
        _, apostila = setup
        url = reverse("apostila", kwargs={"id_apostila": apostila.id})
        client.get(url)
        client.get(url)
        client.get(url)
        total = ViewApostila.objects.filter(apostila=apostila).count()
        assert total == 3
        response = client.get(url)
        assert response.context["views_totais"] == 4

    def test_views_unicas_por_ip_distinct(self, client, setup):
        _, apostila = setup
        # Insere views com IPs misturados manualmente
        ViewApostila.objects.create(ip="5.5.5.5", apostila=apostila)
        ViewApostila.objects.create(ip="5.5.5.5", apostila=apostila)
        ViewApostila.objects.create(ip="6.6.6.6", apostila=apostila)

        unicas = ViewApostila.objects.filter(apostila=apostila).values("ip").distinct().count()
        assert unicas == 2
