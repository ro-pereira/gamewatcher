# GameWatcher — Scraper

Serviço de coleta automatizada de dados do **GameWatcher**, plataforma de consulta de transmissões de jogos de futebol. Este script raspa a agenda de jogos do [ge.globo.com](https://ge.globo.com) e grava as informações diretamente no banco PostgreSQL compartilhado com a API [`gamewatcher-backend`](https://github.com/ro-pereira/gamewatcher-backend).

## Sobre o projeto

O GameWatcher foi desenvolvido para facilitar a consulta de partidas de futebol e suas respectivas opções de transmissão, reunindo em um só lugar informações que normalmente estão espalhadas em diferentes fontes.

Principais funcionalidades e aspectos técnicos do projeto como um todo:

- Interface desenvolvida em React.js e TypeScript
- API REST construída com Node.js e Express
- Persistência e consulta de dados com PostgreSQL
- Web scraping com Selenium para coleta automatizada de informações sobre jogos e transmissões
- Integração entre front-end e API para consumo e apresentação dos dados
- Configuração de CORS para comunicação entre as aplicações
- Interface responsiva e focada na experiência do usuário

## O que este scraper faz

- Percorre a agenda de futebol do ge.globo para os próximos 7 dias
- Para cada partida, abre o modal "Onde assistir?" e extrai:
  - Nome e escudo dos dois times
  - Campeonato/evento
  - Data e horário
  - Canais/opções de transmissão
- Grava times, jogos e canais no PostgreSQL, evitando duplicados (verifica se time, jogo e transmissão já existem antes de inserir)

## Stack

- [Python](https://www.python.org)
- [Selenium](https://www.selenium.dev) (Chrome headless) — automação do navegador
- [webdriver-manager](https://pypi.org/project/webdriver-manager/) — gerencia o ChromeDriver automaticamente
- [psycopg2](https://www.psycopg.org) — conexão com PostgreSQL
- [python-dotenv](https://pypi.org/project/python-dotenv/) — variáveis de ambiente

## Pré-requisitos

- Python 3.9+
- Google Chrome instalado
- Uma instância PostgreSQL acessível, com as tabelas `teams`, `games`, `channels` e `channels_games` já criadas (mesmo banco usado pelo [`gamewatcher-backend`](https://github.com/ro-pereira/gamewatcher-backend))

## Como rodar localmente

1. Clone o repositório:

   ```bash
   git clone https://github.com/ro-pereira/gamewatcher.git
   cd gamewatcher
   ```

2. Crie um ambiente virtual e instale as dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install selenium webdriver-manager psycopg2-binary python-dotenv
   ```

3. Configure as variáveis de ambiente (arquivo `.env` na raiz do projeto):

   ```bash
   DB_HOST=localhost
   DB_NAME=gamewatcher
   DB_USER=usuario
   DB_PASSWORD=senha
   DB_PORT=5432
   ```

4. Rode o scraper:

   ```bash
   python ge_globo_scraper.py
   ```

## Estrutura do projeto

```
├── ge_globo_scraper.py     # Script principal: navega no ge.globo e extrai os dados dos jogos
├── database_wrapper.py     # Camada de acesso ao PostgreSQL (inserts/consultas)
├── request_utils.py        # Funções auxiliares de requisição
├── type.py                 # Estruturas de dados (MatchData, GameInfo)
└── .env                    # Variáveis de conexão com o banco (não versionar credenciais reais)
```

## Repositórios relacionados

- [`gamewatcher-frontend`](https://github.com/ro-pereira/gamewatcher-frontend) — interface web em Next.js/React
- [`gamewatcher-backend`](https://github.com/ro-pereira/gamewatcher-backend) — API REST que expõe os dados coletados por este scraper

## Objetivo do projeto

Desenvolver uma aplicação full-stack completa, integrando desenvolvimento front-end, criação de APIs, persistência de dados e automação de coleta de informações.
