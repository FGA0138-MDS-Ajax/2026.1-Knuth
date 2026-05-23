# Projeto Final - API FastAPI

## Visão geral

Este projeto é uma API REST construída com FastAPI, SQLModel e PostgreSQL, utilizando autenticação OAuth2. A arquitetura segue uma separação clara entre camadas de rotas, serviços, CRUD, modelos e configuração.

## Estrutura do projeto

- `app/main.py`
  - Ponto de entrada da aplicação.
  - Cria a instância FastAPI e registra os routers.
  - Inicia o Uvicorn quando executado diretamente.

- `app/api/v1/routes/`
  - Contém os endpoints da API para `aluno`, `curso`, `usuario` e autenticação.

- `app/services/`
  - Implementa regras de negócio e validações antes das operações no banco.

- `app/crud/`
  - Contém o acesso direto ao banco de dados e operações de Create/Read/Update/Delete.

- `app/models/`
  - Define as tabelas e relações usando SQLModel.

- `app/schemas/`
  - Define os schemas de entrada/saída da API com validação Pydantic.

- `app/core/`
  - `config.py`: configuração baseada em variáveis de ambiente, incluindo `SERVER_PORT`.
  - `database.py`: lógica de conexão com o banco e criação das tabelas.
  - `security.py`: funções de segurança, hash de senha e autenticação.

## Arquitetura

A aplicação usa uma arquitetura em camadas:

1. Rotas (`app/api/v1/routes`): expõem a API para o cliente.
2. Serviços (`app/services`): contêm regras de negócio e validações.
3. CRUD (`app/crud`): acessam e manipulam o banco de dados.
4. Modelos (`app/models`) e Schemas (`app/schemas`): definem a estrutura de dados.
5. Core (`app/core`): configurações, inicialização de banco e segurança.

Isso facilita manutenção, testes e evolução independente de cada camada.

## Requisitos

- Python 3.11+ (recomendado)
- PostgreSQL
- Virtualenv opcional, mas recomendado

## Instalação

1. Clone o repositório:

```bash
git clone <url-do-repositorio>
cd projetoFinal
```

2. Crie e ative o ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente.

Crie um arquivo `.env` na raiz do projeto com algo como:

```env
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seu_banco
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SERVER_PORT=8000
```

## Executando a aplicação

```bash
python3 -m app.main
```
ou
```bash
fastapi dev
```


## URLs úteis

- Documentação automática OpenAPI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## Observações finais

- A aplicação cria as tabelas automaticamente na inicialização via `app/core/database.py`.
- Mantenha a separação entre `routes`, `services`, `crud`, `models` e `schemas` para facilitar futuras manutenções.
