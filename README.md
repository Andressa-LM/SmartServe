# SmartServeAI

Aplicação inteligente de atendimento e recomendação de produtos, desenvolvida como
trabalho acadêmico da **Universidade Veiga de Almeida (UVA)** para a atividade
**AVA 1 — Desenvolvimento de uma aplicação inteligente**.

## Sobre o projeto

O SmartServeAI recebe o nome, o interesse e a mensagem de uma pessoa, consulta
produtos no Mercado Livre e apresenta uma resposta simulada, recomendações e o
prompt preparado para o atendimento. A interface envia os dados ao backend sem
recarregar a página.

O projeto também demonstra tratamento de falha na consulta externa: quando a API
pública não responde ou ocorre um erro de rede, o backend recorre a um pequeno
catálogo local.

## Funcionalidades

- Interface responsiva em HTML5 semântico, com recursos de acessibilidade WAI-ARIA.
- Exemplos de preenchimento rápido para Home Office, Programação e Música.
- API Flask para validar os dados e responder em JSON.
- Busca de até três produtos na API pública do Mercado Livre, com mapeamento de
  interesses e sinônimos.
- Exibição de preços em reais e links para os produtos.
- Resposta demonstrativa gerada localmente, sem integração com um serviço de IA
  generativa.
- Demonstração equivalente pelo terminal.

## Estrutura

```text
SmartServeAI/
├── static/
│   └── css/
│       └── style.css
├── templates/
│   └── index.html
├── .gitignore
├── app.py
├── main.py
├── README.md
└── requirements.txt
```

## Requisitos

- Python instalado.
- Acesso à internet para consultar a API pública do Mercado Livre. Sem conexão,
  o sistema tenta usar o catálogo local de fallback.

## Instalação e execução

No PowerShell, a partir da pasta do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Abra `http://127.0.0.1:5000` no navegador. Para executar a demonstração
interativa no terminal, use:

```powershell
python main.py
```

## API de atendimento

### `POST /api/atendimento`

Recebe JSON com os campos obrigatórios `nome`, `interesse` e `mensagem`:

```json
{
  "nome": "Ana",
  "interesse": "programacao",
  "mensagem": "Procuro produtos para estudar programação."
}
```

Em caso de sucesso, responde com JSON contendo:

- `resposta`: texto do atendimento simulado;
- `produtos`: lista de recomendações, cada uma com identificador, nome, preço,
  link e categoria;
- `prompt`: contexto preparado para uma possível integração futura com IA.

Dados inválidos retornam uma mensagem de erro em JSON e status HTTP `400`.

## Dependências

- Flask `>=3.0.0`
- Requests `>=2.31.0`

## Observação acadêmica

Este repositório é um protótipo didático para a atividade AVA 1 da UVA. A resposta
de IA é simulada; a consulta de produtos usa a API pública do Mercado Livre e
depende da disponibilidade do serviço e da conexão com a internet.
