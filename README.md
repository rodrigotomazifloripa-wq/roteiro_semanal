# Sistema Automático de Roteiros de Conteúdo

## O que é este projeto

Sistema automático que pesquisa notícias de tecnologia aplicada a negócios, gera 3 roteiros completos de conteúdo para LinkedIn e Instagram usando a API do Claude, e envia tudo por e-mail toda **Segunda, Quarta e Sexta às 8h (horário de Brasília)** — sem nenhuma intervenção manual.

Roda como Cron Job no [Render.com](https://render.com) (plano gratuito disponível).

---

## Variáveis de ambiente necessárias

| Variável | Descrição |
|---|---|
| `ANTHROPIC_API_KEY` | Chave da API do Claude (obtenha em console.anthropic.com) |
| `GMAIL_USER` | Endereço Gmail que vai enviar os e-mails (ex: seuemail@gmail.com) |
| `GMAIL_APP_PASSWORD` | Senha de aplicativo do Gmail — **não é sua senha normal** (veja instruções abaixo) |
| `RECIPIENT_EMAIL` | E-mail que vai receber os roteiros (pode ser o mesmo Gmail ou outro) |

---

## Como configurar a senha de app do Gmail

> Você precisa de uma **Senha de App** — é diferente da sua senha normal do Gmail.

1. Acesse [myaccount.google.com](https://myaccount.google.com)
2. Clique em **"Segurança"** no menu lateral
3. Em "Como você faz login no Google", ative a **"Verificação em duas etapas"** se ainda não estiver ativa
4. Após ativar, procure por **"Senhas de app"** (também em "Como você faz login no Google")
5. Selecione **"Outro (nome personalizado)"** e digite `Render Content Bot`
6. Clique em **"Criar"**
7. Copie os **16 caracteres gerados** (sem espaços)
8. Use esse valor como `GMAIL_APP_PASSWORD`

---

## Como subir no Render.com (passo a passo)

1. Crie uma conta gratuita em [render.com](https://render.com)
2. Crie um repositório no GitHub e suba os 3 arquivos: `main.py`, `requirements.txt` e `render.yaml`
3. No Render, clique em **"New +"** → **"Cron Job"**
4. Conecte sua conta do GitHub e selecione o repositório criado
5. O Render detectará automaticamente o `render.yaml` — confirme as configurações
6. Clique em **"Environment"** e adicione as 4 variáveis de ambiente listadas acima
7. Clique em **"Create Cron Job"**
8. Para testar imediatamente: clique em **"Trigger Run"** e verifique o e-mail em alguns minutos

> O agendamento `0 11 * * 1,3,5` equivale a 11h UTC = **8h horário de Brasília (UTC-3)**, toda Segunda (1), Quarta (3) e Sexta (5).

---

## Como testar localmente antes de subir

```bash
pip install -r requirements.txt

# Linux/Mac
export ANTHROPIC_API_KEY="sua_chave_aqui"
export GMAIL_USER="seuemail@gmail.com"
export GMAIL_APP_PASSWORD="sua_senha_app_aqui"
export RECIPIENT_EMAIL="destino@gmail.com"

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sua_chave_aqui"
$env:GMAIL_USER="seuemail@gmail.com"
$env:GMAIL_APP_PASSWORD="sua_senha_app_aqui"
$env:RECIPIENT_EMAIL="destino@gmail.com"

python main.py
```

---

## O que o sistema faz, passo a passo

1. Busca até 30 artigos recentes usando 6 queries no DuckDuckGo (sem precisar de API key)
2. Monta um prompt com as notícias e envia para o Claude (`claude-opus-4-6`)
3. O Claude gera 3 roteiros completos — LinkedIn e Instagram — prontos para usar
4. Converte o conteúdo em HTML bem formatado e envia por e-mail via Gmail SMTP

---

## Estrutura do projeto

```
conteudo-auto/
├── main.py          # Lógica principal: busca, geração e envio
├── requirements.txt # Dependências Python
├── render.yaml      # Configuração do Cron Job no Render
└── README.md        # Este arquivo
```
