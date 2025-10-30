# AluConnect

**AluConnect** é uma plataforma educacional desenvolvida com Django REST Framework, PostgreSQL e autenticação via JWT e OAuth2. Ela conecta alunos, instrutores e cursos em um ambiente seguro e escalável, com suporte a progresso de aprendizado, emissão de certificados e integração com login social.

```
AluConnect
├── apps
│   ├── certificates
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── constants.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── courses
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── permissions.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── instructors
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── lessons
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── services/
│   │   └── tests/
│   ├── progress
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── constants.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── services/
│   │   └── tests/
│   ├── students
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   └── users
│       ├── admin.py
│       ├── apps.py
│       ├── constants.py
│       ├── models.py
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py
│       └── tests/
├── config
│   ├── asgi.py
│   ├── celery.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── utils.py
│   ├── views.py
│   └── wsgi.py
├── data
├── staticfiles/
├── manage.py
├── rundata.py
├── requirements.txt
├── pytest.ini
├── docker-compose.yml
├── Dockerfile
├── LICENSE
└── README.md
```

---

## Funcionalidades

- Cadastro e autenticação de usuários com JWT e Google OAuth2
- Gestão de cursos e aulas com CRUD completo
- Matrícula de alunos e associação com instrutores
- Registro de progresso por aula e por curso
- Emissão de certificados ao concluir cursos
- Sistema de permissões por papel (aluno, instrutor, admin)
- Logout com blacklist de tokens
- Integração com Celery e Redis para tarefas assíncronas
- Geração automática de certificados personalizados usando modelo de linguagem (LLM), com base no nome do aluno, curso concluído e data de finalização

---

## Tecnologias utilizadas

- Django 5.2 + Django REST Framework
- PostgreSQL 15
- Docker + Docker Compose
- Celery + Redis
- JWT (SimpleJWT)
- Google OAuth2 (social-auth-app-django)
- Gunicorn
- Python 3.10

---

## Como executar o projeto

### Clone o repositório

```bash
git clone https://github.com/mariacarolinass/aluconnect.git
cd aluconnect
```

### Crie o arquivo .env

```bash
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

JWT_ACCESS_LIFETIME=5
JWT_REFRESH_LIFETIME=30

GOOGLE_CLIENT_ID=key.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

DB_ENGINE=django.db.backends.postgresql
DB_NAME=aluconnect_db
DB_USER=aluconnect_carol
DB_PASSWORD=1234
DB_HOST=db
DB_PORT=5432

OPENAI_API_KEY=your-openai-api-key

CELERY_BROKER_URL=redis://redis:6379/0
```

Caso queira utilizar SQLite ao invés de PostgreSQL, comente as variáveis relacionadas ao banco de dados PostgreSQL e adicione as linhas abaixo:

```bash
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

O SQLite facilita a execução local sem a necessidade de configurar um banco de dados separado e é útil para testes rápidos ou desenvolvimento inicial sem o Docker.

### Execute com Docker

```bash
docker-compose up --build
```

Caso seja necessário suba as migrações para funcionar:

```bash
docker-compose run --rm web python manage.py migrate
```

Em caso de conflitos de migrações utilize:

```bash
python manage.py makemigrations --merge
```

#### Acesse no navegador

```bash
http://localhost:8000/
```

### Execute localmente (fora do Docker)

1. Ative o ambiente virtual

```bash
source .venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Instale as dependências

```bash
pip install -r requirements.txt
```

3. Crie as migrações

```bash
python manage.py makemigrations
```

4. Aplique as migrações

```bash
python manage.py migrate
```

5. Rode a aplicação

```bash
python manage.py runserver
```

#### Acesse no navegador

```bash
http://127.0.0.1:8000/
```

## Documentação da API com Swagger

A API do AluConnect é documentada automaticamente com o pacote drf-spectacular, permitindo que qualquer pessoa visualize e teste os endpoints diretamente no navegador.

### Como acessar

Após subir o projeto, acesse:

- Swagger UI: `/api/docs/`
- Redoc: `/api/redoc/`
- Schema JSON: `/api/schema/`

### Testes com autenticação

Para testar endpoints protegidos:

1. Clique em Authorize no topo da interface Swagger

2. Insira seu token JWT no formato:

```bash
Bearer <seu_access_token>
```

3. Os endpoints protegidos estarão liberados para teste

## Importando dados para o banco

O arquivo `rundata.py` importa os dados em csv do diretório `data` para o banco de dados.

### Importe para o banco no Docker

```bash
docker-compose run --rm web python rundata.py
```

### Importe para o banco local

```bash
python rundata.py
```

## Como rodar os testes

### Rodando testes com Docker

```bash
docker-compose run web pytest
```

### Rodando testes localmente (fora do Docker)

Rode todos os testes com:

```bash
pytest
```

Ou rodar testes específicos:

```bash
pytest apps/users/tests/test_auth.py
```

Para visualizar a cobertura de código:

```bash
pytest --cov=apps
```

## Principais decisões de design

- JWT com refresh token e blacklist para segurança e escalabilidade
- Separação por apps (users, courses, students, progress, lessons, instructors, certificates) para modularidade
- Docker Compose com serviços isolados (web, db, redis, celery) para facilitar deploy e desenvolvimento
- Customização de erros e respostas para melhorar a experiência da API
- Uso de Celery para tarefas como envio de certificados
- Autenticação social com Google para facilitar onboarding

### LLM

- Uso de modelo de linguagem (LLM) para gerar certificados com texto personalizado, evitando templates fixos e permitindo variações criativas e formais
- O certificado é gerado com base no progresso do aluno, validando se todas as aulas foram concluídas antes da emissão
