import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import DO_NOTHING, GenericIPAddressField

from apostilas.models import Apostila, ViewApostila


# ==============================================================================
# TESTES DE MODELS - apostilas/models.py
# ==============================================================================

@pytest.mark.django_db
class TestApostilaModel:

    @pytest.fixture
    def usuario(self):
        return User.objects.create_user(username="apostilauser", password="senha123")

    def test_criacao_apostila(self, usuario):
        arquivo = SimpleUploadedFile("apostila.pdf", b"conteudo do arquivo", content_type="application/pdf")
        apostila = Apostila.objects.create(
            user=usuario,
            titulo="Apostila de Python",
            arquivo=arquivo,
        )
        assert apostila.titulo == "Apostila de Python"
        assert apostila.user == usuario

    def test_str_apostila(self, usuario):
        apostila = Apostila(user=usuario, titulo="Guia de Django")
        assert str(apostila) == "Guia de Django"

    def test_titulo_max_length(self):
        field = Apostila._meta.get_field("titulo")
        assert field.max_length == 100

    def test_arquivo_upload_to(self):
        field = Apostila._meta.get_field("arquivo")
        assert field.upload_to == "apostilas"

    def test_user_on_delete_do_nothing(self):
        field = Apostila._meta.get_field("user")
        assert field.remote_field.on_delete == DO_NOTHING


@pytest.mark.django_db
class TestViewApostilaModel:

    @pytest.fixture
    def apostila(self):
        user = User.objects.create_user(username="viewapostilauser", password="senha123")
        arquivo = SimpleUploadedFile("doc.pdf", b"pdf", content_type="application/pdf")
        return Apostila.objects.create(user=user, titulo="Apostila Teste", arquivo=arquivo)

    def test_criacao_view_apostila(self, apostila):
        view = ViewApostila.objects.create(ip="192.168.0.1", apostila=apostila)
        assert view.ip == "192.168.0.1"
        assert view.apostila == apostila

    def test_str_view_apostila(self, apostila):
        view = ViewApostila(ip="10.0.0.1", apostila=apostila)
        assert str(view) == "10.0.0.1"

    def test_multiplas_views_mesma_apostila(self, apostila):
        ViewApostila.objects.create(ip="192.168.0.1", apostila=apostila)
        ViewApostila.objects.create(ip="192.168.0.2", apostila=apostila)
        ViewApostila.objects.create(ip="192.168.0.1", apostila=apostila)  # IP repetido
        total = ViewApostila.objects.filter(apostila=apostila).count()
        assert total == 3

    def test_views_unicas_por_ip(self, apostila):
        ViewApostila.objects.create(ip="10.0.0.1", apostila=apostila)
        ViewApostila.objects.create(ip="10.0.0.1", apostila=apostila)
        ViewApostila.objects.create(ip="10.0.0.2", apostila=apostila)
        unicas = ViewApostila.objects.filter(apostila=apostila).values("ip").distinct().count()
        assert unicas == 2

    def test_apostila_on_delete_do_nothing(self):
        field = ViewApostila._meta.get_field("apostila")
        assert field.remote_field.on_delete == DO_NOTHING

    def test_ip_e_campo_generico(self):
        field = ViewApostila._meta.get_field("ip")
        assert isinstance(field, GenericIPAddressField)
