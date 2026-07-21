# CNPJ Insight

> Sistema profissional para consulta, persistência e gerenciamento de informações de CNPJ utilizando Python, FastAPI, SQLModel e SQLite.


![Python](https://img.shields.io/badge/Python-3.12-blue)  ![FastAPI](https://img.shields.io/badge/FastAPI-0.139-green)  ![Tests](https://img.shields.io/badge/Tests-39%20passed-success)  ![Coverage](https://img.shields.io/badge/Coverage-94%25-success)


> 🚧 Projeto em desenvolvimento contínuo

---

## Status do Projeto

O **CNPJ Insight** possui sua base técnica consolidada, com as principais camadas da aplicação implementadas e validadas por testes automatizados.

Atualmente o projeto conta com:

- ✅ Consulta de CNPJ
- ✅ Persistência em banco SQLite
- ✅ Histórico de consultas
- ✅ Sistema de Favoritos
- ✅ Estatísticas das consultas
- ✅ API REST com FastAPI
- ✅ Documentação automática (Swagger e ReDoc)
- ✅ Testes automatizados
- ✅ Integração Contínua (GitHub Actions)
- ✅ Cobertura de testes superior a 90%
- ✅ Análise estática com Ruff
- ✅ Verificação de tipos com Mypy

---

# Objetivo

O **CNPJ Insight** foi desenvolvido para oferecer uma solução robusta, performática e escalável para consulta e gerenciamento de informações cadastrais de empresas brasileiras.

O projeto utiliza arquitetura em camadas, separando responsabilidades entre persistência, regras de negócio e API, facilitando evolução, manutenção e testes.

---

# Funcionalidades Implementadas

### Consulta de CNPJ

Consulta informações cadastrais utilizando API pública.

### Histórico

Armazena automaticamente todas as consultas realizadas.

### Favoritos

Permite marcar empresas para acesso rápido.

### Estatísticas

Gera indicadores sobre as consultas realizadas.

### API REST

Endpoints documentados automaticamente utilizando FastAPI.

### Documentação Interativa

- Swagger UI

  
- ReDoc

---

# Roadmap

As funcionalidades abaixo fazem parte da evolução planejada do projeto.

- Dashboard de indicadores
- Comparador de empresas
- Exportação de dados
- JSON Viewer
- Interface Web
- Autenticação de usuários

---

# Arquitetura

```
cnpj-insight/
│
├── app/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── utils/
│   └── main.py
│
├── tests/
│
├── .github/
│   └── workflows/
│
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── README.md
└── LICENSE
```

---

# Tecnologias

- Python 3.12+
- FastAPI
- SQLModel
- SQLAlchemy
- SQLite
- HTTPX
- Pytest
- Pytest-Cov
- Ruff
- Mypy
- GitHub Actions

---

# Pré-requisitos

- Python 3.12+
- Git
- pip
- Conexão com a Internet

---

# Instalação

Clone o projeto:

```bash
git clone https://github.com/wagner-wrr/cnpj-insight.git
```

Entre no diretório:

```bash
cd cnpj-insight
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente:

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

# Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto.

Exemplo:

```text
DATABASE_URL=sqlite:///./cnpj_insight.db
API_URL=https://publica.cnpj.ws/cnpj
```

---

# Executando a aplicação

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

```
http://localhost:8000
```

---

# Documentação da API

Swagger

```
http://localhost:8000/docs
```

![Imagem Swegger](https://github.com/wagner-wrr/cnpj-insight/blob/main/assents/images/Swegger%20-%201.jpeg)

ReDoc

```
http://localhost:8000/redoc
```

![Imagem Redocs](https://github.com/wagner-wrr/cnpj-insight/blob/main/assents/images/Redocs%20-1.jpeg)
![Imagem Redocs](https://github.com/wagner-wrr/cnpj-insight/blob/main/assents/images/Redocs%20-%202.jpeg)
![Imagem Redocs](https://github.com/wagner-wrr/cnpj-insight/blob/main/assents/images/Redocs%20-%203.jpeg)
![Imagem Redocs](https://github.com/wagner-wrr/cnpj-insight/blob/main/assents/images/Redocs%20-%204.jpeg)
![Imagem Redocs](https://github.com/wagner-wrr/cnpj-insight/blob/main/assents/images/Redocs%20-%205.jpeg)
![Imagem Redocs](https://github.com/wagner-wrr/cnpj-insight/blob/main/assents/images/Redocs%20-%206.jpeg)

---

# Testes

Executar todos os testes:

```bash
pytest
```

Executar testes com cobertura:

```bash
pytest -v --tb=short --cov=app --cov-report=term-missing --cov-fail-under=70
```

---

# Qualidade de Código

Lint

```bash
ruff check .
```

Correção automática

```bash
ruff check . --fix
```

Verificação de tipos

```bash
python -m mypy app
```

---

# Integração Contínua

O projeto utiliza **GitHub Actions** para validação automática.

A cada Push ou Pull Request são executados:

- Ruff
- Pytest
- Cobertura de testes
- Mypy

Caso qualquer etapa falhe, o workflow é interrompido automaticamente.

---

# Fluxo de Desenvolvimento

- Branch principal protegida (`main`)
- Pull Requests obrigatórios
- Aprovação antes do merge
- Execução automática do CI

---

# Próximos Passos

- Dashboard estatístico
- Comparador de empresas
- Exportação de dados
- Interface Web
- Melhorias de performance
- Ampliação dos testes de integração

---

# Segurança

- Nunca versione arquivos `.env`
- Nunca publique credenciais
- Utilize `.gitignore` atualizado
- Não versione bancos SQLite locais

---

# Licença

Este projeto está licenciado sob a **Licença MIT**.

Consulte o arquivo **LICENSE** para mais informações.

---

# Autor

**Wagner Rodrigues Ramos**

**Python FullStack Developer**

GitHub:
https://github.com/wagner-wrr

LinkedIn:
https://linkedin.com/in/wagner-wrr
