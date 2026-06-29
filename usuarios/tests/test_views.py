import pytest
from django.contrib.auth.models import User
from django.urls import reverse


# ==============================================================================
# TESTES DE VIEWS - usuarios/views.py
# ==============================================================================

@pytest.mark.django_db
class TestCadastroView:

    def test_get_retorna_formulario(self, client):
        url = reverse("cadastro")
        response = client.get(url)
        assert response.status_code == 200
        assert "form" in response.context

    def test_usuario_autenticado_redireciona(self, client):
        User.objects.create_user(username="jaexiste", password="senha123")
        client.login(username="jaexiste", password="senha123")
        url = reverse("cadastro")
        response = client.get(url)
        assert response.status_code == 302

    def test_post_cadastro_valido_cria_usuario(self, client):
        url = reverse("cadastro")
        data = {
            "username": "novousuario",
            "email": "novo@email.com",
            "password1": "SenhaForte@123",
            "password2": "SenhaForte@123",
        }
        response = client.post(url, data)
        assert response.status_code == 302
        assert User.objects.filter(username="novousuario").exists()

    def test_post_senhas_diferentes_nao_cria_usuario(self, client):
        url = reverse("cadastro")
        data = {
            "username": "usuario2",
            "email": "u2@email.com",
            "password1": "SenhaForte@123",
            "password2": "SenhaDiferente@456",
        }
        response = client.post(url, data)
        assert response.status_code == 200  # Re-renderiza o form com erros
        assert not User.objects.filter(username="usuario2").exists()


@pytest.mark.django_db
class TestLoginView:

    @pytest.fixture
    def usuario(self):
        return User.objects.create_user(
            username="loginuser", email="login@email.com", password="Senha@123"
        )

    def test_get_retorna_formulario(self, client):
        url = reverse("login")
        response = client.get(url)
        assert response.status_code == 200

    def test_usuario_autenticado_redireciona(self, client, usuario):
        client.login(username="loginuser", password="Senha@123")
        url = reverse("login")
        response = client.get(url)
        assert response.status_code == 302

    def test_login_com_username_valido(self, client, usuario):
        url = reverse("login")
        data = {"userinput": "loginuser", "password": "Senha@123"}
        response = client.post(url, data)
        assert response.status_code == 302

    def test_login_com_email_valido(self, client, usuario):
        url = reverse("login")
        data = {"userinput": "login@email.com", "password": "Senha@123"}
        response = client.post(url, data)
        assert response.status_code == 302

    def test_login_com_senha_errada_redireciona_com_erro(self, client, usuario):
        url = reverse("login")
        data = {"userinput": "loginuser", "password": "SenhaErrada"}
        response = client.post(url, data)
        assert response.status_code == 302
        assert "login" in response["Location"]

    def test_login_usuario_inexistente(self, client):
        url = reverse("login")
        data = {"userinput": "naoexiste", "password": "qualquercoisa"}
        response = client.post(url, data)
        assert response.status_code == 302
        assert "login" in response["Location"]


@pytest.mark.django_db
class TestLogoutView:

    def test_logout_desloga_e_redireciona(self, client):
        User.objects.create_user(username="sairuser", password="Senha@123")
        client.login(username="sairuser", password="Senha@123")
        url = reverse("logout")
        response = client.get(url)
        assert response.status_code == 302
        assert "login" in response["Location"]

    def test_logout_sem_autenticacao_redireciona(self, client):
        url = reverse("logout")
        response = client.get(url)
        assert response.status_code == 302
