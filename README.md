<div align="center" id="top"> 
  <h1>Study Async</h1>
</div>

<p align="center">
  <a href="#sobre">Sobre</a> &#xa0; | &#xa0; 
  <a href="#funcionalidades">Funcionalidades</a> &#xa0; | &#xa0;
  <a href="#tecnologias">Tecnologias</a> &#xa0; | &#xa0;
  <a href="#pre-requisitos">Pré-requisitos</a> &#xa0; | &#xa0;
  <a href="#rodando-testes">Começando</a>
</p>

## <div id="sobre">🎯 Sobre</div>

Aplicação web em Django para criação e estudo de flashcards, organizados por categoria e nível de dificuldade, com desafios cronometrados, relatórios de desempenho e repositório de apostilas em PDF.

## <div id="funcionalidades">✨ Funcionalidades</div>

✔️ **Cadastro e login de usuários** (via username ou e-mail)\
✔️ **Flashcards**: criação, listagem e exclusão, organizados por categoria e dificuldade (Fácil, Médio, Difícil)\
✔️ **Desafios**: monte um desafio escolhendo categorias, dificuldade e quantidade de perguntas; o sistema sorteia os flashcards automaticamente\
✔️ **Relatórios**: acompanhe acertos, erros e desempenho por categoria em cada desafio\
✔️ **Apostilas**: upload de arquivos (PDF e outros), com contagem de visualizações totais e únicas (por IP)

## <div id="tecnologias">🚀 Tecnologias</div>

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [SQLite](https://www.sqlite.org/index.html)
- [PyTest](https://docs.pytest.org/en/stable/)

## Estrutura do projeto

```
study_async/
├── flashcard/      # Flashcards, categorias e desafios
├── apostilas/      # Upload e visualização de apostilas
├── usuarios/       # Cadastro, login e logout
├── core/           # Configurações gerais do Django
└── manage.py
```

## Instalação

### <div id="pre-requisitos">✅ Pré-requisitos</div>

- Python 3.10+ instalado
- Git

### 1. Clone o repositório

```bash
git clone https://github.com/raphael-araujo/study_async.git
cd study_async
```

### 2. Crie e ative um ambiente virtual

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (Git Bash):**
```bash
python -m venv venv
source venv/Scripts/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

[//]: # (### 4. Configure as variáveis de ambiente)

[//]: # ()
[//]: # (Crie um arquivo `.env` na raiz do projeto com as variáveis necessárias, por exemplo:)

[//]: # ()
[//]: # (```env)

[//]: # (SECRET_KEY=sua-chave-secreta-aqui)

[//]: # (DEBUG=True)

[//]: # (ALLOWED_HOSTS=localhost,127.0.0.1)

[//]: # (```)

[//]: # ()
[//]: # (> Ajuste as variáveis conforme o `settings.py` do projeto. Se o projeto usa `django-environ` ou `python-decouple`, confirme o nome exato das chaves esperadas.)

### 4. Aplique as migrations

```bash
python manage.py migrate
```

### 5. Crie um superusuário (opcional, para acessar o admin)

```bash
python manage.py createsuperuser
```

### 6. Rode o servidor de desenvolvimento

```bash
python manage.py runserver
```

A aplicação estará disponível em `http://127.0.0.1:8000/`.

## <div id="rodando-testes">Rodando os testes</div>

O projeto utiliza **PyTest** com **pytest-django**.

### 1. Instale as dependências de teste (se ainda não instaladas)

```bash
pip install pytest pytest-django
```

### 2. Execute os testes

```bash
# Todos os testes
pytest

# Com mais detalhes
pytest -v

# Um arquivo específico
pytest test_apostilas.py -v

# Um teste específico
pytest test_apostilas.py::TestApostilaModel::test_str_apostila -v

# Reutilizando o banco de testes (mais rápido em execuções repetidas)
pytest --reuse-db
```

## Modelos principais

| App | Modelo | Descrição |
|---|---|---|
| `flashcard` | `Categoria` | Categoria de um flashcard |
| `flashcard` | `Flashcard` | Pergunta/resposta associada a um usuário e categoria |
| `flashcard` | `Desafio` | Conjunto de flashcards sorteados para um desafio |
| `flashcard` | `FlashcardDesafio` | Estado de um flashcard dentro de um desafio (respondido/acertou) |
| `apostilas` | `Apostila` | Arquivo enviado por um usuário |
| `apostilas` | `ViewApostila` | Registro de visualização de uma apostila (por IP) |


&#xa0;

<a href="#top">Voltar para o topo</a>
