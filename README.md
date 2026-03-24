# mastermind-fullstack

Aplicacao web full-stack do jogo Mastermind, com autenticacao, historico de partidas, ranking e tabuleiro visual no frontend.

## Visao geral

O projeto foi organizado em duas pastas na raiz:

- `backend/`: API FastAPI com autenticacao JWT, persistencia em banco relacional, ranking e regras do jogo
- `frontend/`: aplicacao Angular com login, registro, dashboard, ranking e tela de jogo

## Decisoes tecnicas

- Backend em `Python + FastAPI + SQLAlchemy`
- Frontend em `Angular 17`
- Banco local padrao com `SQLite` para facilitar execucao do case
- Autenticacao via `JWT Bearer Token`
- Persistencia de:
  - usuarios
  - partidas
  - tentativas
  - score final
  - duracao da partida
  - melhor score do usuario
- Estrutura do backend separada em:
  - routers
  - services
  - repositories
  - models
  - schemas

## Requisitos atendidos

- Login e registro com validacao
- Logout com redirecionamento
- Dashboard inicial
- Jogo funcional com ate 10 tentativas
- Backend gera codigo unico da partida e segredo da rodada
- Frontend nunca recebe a combinacao correta durante a partida
- Historico completo das tentativas
- Ranking por desempenho
- Testes de backend e frontend
- API documentada via Swagger/OpenAPI

## Pre-requisitos

### Backend

- Python 3.12+ ou compativel

### Frontend

- Node.js 18+
- npm 9+

Observacao:

- O frontend foi ajustado para rodar com Node 18 neste ambiente.
- Os testes do frontend usam o Brave instalado localmente como browser headless.

## Variaveis de ambiente

Use o arquivo `backend/.env.example` como base para criar o `backend/.env`.

Exemplo atual:

```env
APP_NAME=Mastermind API
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000

DATABASE_URL=sqlite:///./mastermind.db

JWT_SECRET=change_me
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

CORS_ALLOWED_ORIGINS=http://localhost:4200
```

## Como rodar o backend

No terminal:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

API:

- `http://127.0.0.1:8000`

Swagger:

- `http://127.0.0.1:8000/docs`

Observacao:

- Se voce tiver um arquivo `backend/mastermind.db` de uma versao antiga do projeto, apague-o antes de subir a API para recriar o schema local com os campos mais recentes.

## Como rodar o frontend

Em outro terminal:

```powershell
cd frontend
npm install
npm start
```

Aplicacao:

- `http://localhost:4200`

O frontend esta configurado para consumir:

- `http://127.0.0.1:8000/api`

## Como rodar os testes

### Backend

```powershell
cd backend
.\.venv\Scripts\python.exe -m pytest
```

### Frontend

```powershell
cd frontend
npm test
```

## Fluxo principal da aplicacao

1. Criar conta em `/register`
2. Fazer login em `/login`
3. Ir para `/home`
4. Iniciar uma nova partida
5. Jogar em `/games/:code`
6. Consultar o ranking em `/ranking`

## API principal

### Auth

- `POST /api/auth/register`
- `POST /api/auth/login`

### Games

- `POST /api/games`
- `GET /api/games/{game_code}`
- `POST /api/games/{game_code}/guess`
- `GET /api/games/{game_code}/attempts`
- `GET /api/games/ranking/list`

## Ranking

O ranking e ordenado por:

1. melhor score
2. numero de vitorias
3. nome do jogador

## Regras implementadas

- O segredo possui 4 cores
- Cores validas:
  - `R`
  - `G`
  - `B`
  - `Y`
  - `O`
  - `P`
- O jogador possui no maximo 10 tentativas
- O backend retorna apenas a quantidade de acertos exatos por jogada
- A partida termina quando:
  - o jogador acerta as 4 posicoes
  - ou esgota as tentativas

## Diferenciais entregues

- Tabuleiro visual estilo Mastermind
- Guard e interceptor JWT no frontend
- Tratamento global de excecoes no backend
- Ranking funcional
- Persistencia de score final e duracao da partida

## Melhorias futuras

- Feedback completo estilo Mastermind real:
  - cor certa no lugar certo
  - cor certa na posicao errada
- Exibir codigo secreto ao fim da derrota
- Separar componentes do tabuleiro em subcomponentes
- Alembic para migracoes formais em vez de `create_all`
- Testes de interface mais amplos no frontend

## Demonstracao visual

Fluxos principais do MVP em execucao local.

### Login

Tela de autenticacao com validacao e redirecionamento para o dashboard.

![Login](docs/assets/login.gif)

### Registro

Criacao de conta para novo jogador.

![Registro](docs/assets/register.gif)

### Dashboard

Painel inicial com acesso rapido para nova partida e ranking.

![Dashboard](docs/assets/dashboard.gif)

### Jogo em andamento

Tabuleiro visual estilo Mastermind com envio de palpites e feedback por rodada.

![Gameplay](docs/assets/gameplay.gif)

### Ranking

Listagem ordenada por melhor score e desempenho dos jogadores.

![Ranking](docs/assets/ranking.gif)
