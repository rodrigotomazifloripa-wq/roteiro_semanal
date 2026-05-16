import anthropic
from ddgs import DDGS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import traceback
from datetime import datetime
import re
import markdown as md_lib

DIAS_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo",
}

QUERIES = [
    # Tendências globais de tecnologia para negócios
    "AI agents autonomous business tools 2026",
    "small business software trends 2026",
    # Setores específicos brasileiros
    "tecnologia para restaurantes bares delivery 2026",
    "sistema para clínicas médicas odontológicas software",
    "automação para salão de beleza estética gestão",
    "tecnologia para academia fitness gestão clientes",
    # Vendas e marketing digital
    "WhatsApp Business API automação vendas novidades",
    "tráfego pago inteligência artificial Google Meta ads",
    "ecommerce ferramentas conversão abandonamento carrinho",
    # Eficiência operacional e financeira
    "gestão financeira pequena empresa app controle",
    "estoque automático reposição inteligente varejo",
    "nota fiscal eletrônica integração sistema gestão",
    # Cases e tendências internacionais
    "retail technology innovation store 2026",
    "customer service chatbot ROI small business case",
]


def search_news():
    results = []
    try:
        with DDGS() as ddgs:
            for query in QUERIES:
                try:
                    articles = ddgs.news(query, timelimit="w", max_results=5)
                    for article in articles:
                        results.append(
                            {
                                "title": article.get("title", ""),
                                "body": article.get("body", ""),
                                "source": article.get("source", ""),
                                "date": article.get("date", ""),
                                "url": article.get("url", ""),
                            }
                        )
                except Exception as e:
                    print(f"Erro ao buscar query '{query}': {e}")
    except Exception as e:
        print(f"Erro geral na busca de notícias: {e}")

    # remove duplicatas pelo título
    seen = set()
    unique = []
    for r in results:
        key = r["title"].strip().lower()
        if key and key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def generate_content(news_results):
    now = datetime.now()
    dia_semana = DIAS_SEMANA[now.weekday()]
    data_hoje = now.strftime(f"%d/%m/%Y ({dia_semana})")

    news_lines = []
    for i, article in enumerate(news_results[:25]):
        news_lines.append(f"TÍTULO: {article['title']}")
        news_lines.append(f"RESUMO: {article['body']}")
        news_lines.append(f"FONTE: {article['source']}")
        news_lines.append(f"DATA: {article['date']}")
        news_lines.append("---")
    news_text = "\n".join(news_lines) if news_lines else "Nenhuma notícia encontrada — use seu conhecimento atualizado sobre tendências de tecnologia para negócios em 2026."

    prompt = f"""Você é um assistente de criação de conteúdo para Rodrigo, desenvolvedor brasileiro que usa LinkedIn e Instagram para atrair empresários, comerciantes e donos de negócio como potenciais clientes — pessoas que podem contratar seus serviços de desenvolvimento ou comprar sistemas que ele cria.

O objetivo dos posts NÃO é falar para outros devs. É mostrar para empresários como a tecnologia pode resolver problemas reais do negócio deles: aumentar vendas, reduzir custos, automatizar processos, atender melhor os clientes — e posicionar o Rodrigo como o especialista certo para implementar essas soluções.

## NOTÍCIAS E TENDÊNCIAS PESQUISADAS HOJE

{news_text}

## SUA TAREFA

Com base nas notícias acima, crie 6 roteiros completos para a semana — um por dia útil (segunda a sábado).

### REGRAS DE VARIEDADE — OBRIGATÓRIAS:
- As 6 opções DEVEM ser de segmentos ou ângulos completamente diferentes entre si. Proibido repetir o mesmo assunto, setor ou abordagem em mais de uma opção.
- Cada opção deve falar para um tipo diferente de empresário (ex: dono de restaurante, gestor de clínica, lojista de varejo, dono de academia, prestador de serviços, empresário do agronegócio — varie sempre).
- Priorize temas INESPERADOS e CONCRETOS. Evite os óbvios ("IA vai mudar tudo", "digitalização é importante"). Prefira: "farmácias que usam X aumentaram Y%", "este erro custa R$Z por mês para o seu negócio", "ferramenta desconhecida que seu concorrente já usa".
- Use dados reais das notícias sempre que possível. Se não houver dado, crie uma situação concreta e verossímil.
- O tom deve variar entre as 6 opções: misture provocativo, educativo, de case/resultado, de urgência, de curiosidade e de comparação.

### CRITÉRIOS DE QUALIDADE POR OPÇÃO:
1. Ser diretamente relevante para donos de negócio, comerciantes ou gestores (NÃO para devs)
2. Ter uma aplicação prática clara ("com isso você pode economizar X", "seu cliente recebe resposta em Y segundos", etc.)
3. Despertar curiosidade ou urgência ("quem ainda não usa está perdendo dinheiro", "seu concorrente já faz isso", etc.)
4. Abrir naturalmente uma porta para o empresário pensar: "preciso disso — vou falar com o Rodrigo"

Para cada opção, escolha o formato mais adequado:
- **Post estático**: melhor para dados impactantes, reflexões, perguntas provocativas, comparações rápidas
- **Carrossel (4 a 7 slides)**: melhor para passo a passo, lista de benefícios, antes/depois, "X erros que custam dinheiro"
- **Vídeo curto (1 a 2 min)**: melhor para novidades quentes, demonstrações, conversa direta com o empresário

## FORMATO DE ENTREGA

Entregue as 6 opções no formato abaixo, sem resumir, sem cortar — completo para uso imediato:

---

# 📅 ROTEIROS DE CONTEÚDO — {data_hoje}

---

## ✅ OPÇÃO 1 — {{TÍTULO DO TEMA}}

**🎯 Por que este tema agora:** {{2 frases explicando relevância e urgência para o empresário}}
**📌 Formato recomendado:** {{Post estático / Carrossel de X slides / Vídeo de ~X min}}
**⏱️ Tempo estimado de produção:** {{Ex: 15 minutos}}

### 🔵 LINKEDIN

**Hook (primeira linha):**
{{Frase de abertura poderosa — dado chocante, pergunta, ou afirmação forte que para o scroll}}

**Texto completo:**
{{Post completo pronto para colar no LinkedIn. Parágrafos curtos, 1-2 linhas cada. Tom de especialista que entende de negócio E de tecnologia — não de programador. Termina com CTA sutil como "Se quiser saber como aplicar isso no seu negócio, me manda uma mensagem."}}

**Hashtags:**
{{6 hashtags relevantes}}

---

### 🟣 INSTAGRAM

**Caption:**
{{Versão curta e direta, máximo 120 palavras, com 3 a 5 emojis e CTA para direct ou link na bio}}

**Sugestão de visual/capa:**
{{Descrição específica do que montar no Canva em menos de 10 minutos — cor de fundo, ícone, título principal, subtítulo}}

{{SE CARROSSEL, inclua:}}
**Roteiro dos slides:**
- 📌 Slide 1 (CAPA): {{título + subtítulo}}
- 📌 Slide 2: {{conteúdo}}
- 📌 Slide 3: {{conteúdo}}
... (todos os slides)
- 📌 Último slide: {{CTA — ex: "Quer automatizar isso no seu negócio? Me chama no direct 👇"}}

{{SE VÍDEO, inclua:}}
**Roteiro de fala:**
- 🎬 Abertura (0:00–0:15): {{exatamente o que falar — gancho forte}}
- 🎬 Desenvolvimento: {{cada ponto em bullet, o que falar em cada um}}
- 🎬 CTA final (últimos 15s): {{exatamente o que falar para chamar para ação}}

---

## ✅ OPÇÃO 2 — {{TÍTULO DO TEMA}}
{{mesmo formato completo acima}}

---

## ✅ OPÇÃO 3 — {{TÍTULO DO TEMA}}
{{mesmo formato completo acima}}

---

## ✅ OPÇÃO 4 — {{TÍTULO DO TEMA}}
{{mesmo formato completo acima}}

---

## ✅ OPÇÃO 5 — {{TÍTULO DO TEMA}}
{{mesmo formato completo acima}}

---

## ✅ OPÇÃO 6 — {{TÍTULO DO TEMA}}
{{mesmo formato completo acima}}

---

## 💡 RECOMENDAÇÃO DA SEMANA
{{Qual das 6 opções você recomenda para começar a semana, por quê em 3 frases, e uma dica rápida de execução}}

---

Tom geral: direto, acessível, sem jargão técnico. Rodrigo é o cara que resolve o problema do empresário — não só o cara que programa. Cada post deve fazer o leitor pensar "preciso disso no meu negócio" e lembrar que existe uma pessoa que pode implementar.
"""

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    for tentativa in range(3):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=16000,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except anthropic.InternalServerError as e:
            if tentativa < 2:
                print(f"Erro temporário da API (tentativa {tentativa + 1}/3), aguardando 10s...")
                import time
                time.sleep(10)
            else:
                raise e


def _markdown_to_html(text):
    converted = md_lib.markdown(text, extensions=["nl2br"])
    return converted


def send_email(content):
    gmail_user = os.environ["GMAIL_USER"]
    gmail_password = os.environ["GMAIL_APP_PASSWORD"]
    recipient = os.environ["RECIPIENT_EMAIL"]

    now = datetime.now()
    dia_semana = DIAS_SEMANA[now.weekday()]
    date_str = now.strftime("%d/%m/%Y")
    subject = f"📱 Roteiros de Conteúdo para Hoje — {date_str} ({dia_semana})"

    html_body = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  body {{
    font-family: Arial, sans-serif;
    font-size: 15px;
    background-color: #f5f5f5;
    margin: 0;
    padding: 20px;
    color: #333;
  }}
  .wrapper {{
    max-width: 800px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 8px;
    padding: 30px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  }}
  h1 {{
    color: #1a1a2e;
    font-size: 22px;
    border-bottom: 2px solid #1a1a2e;
    padding-bottom: 10px;
  }}
  h2 {{
    color: #1a1a2e;
    font-size: 18px;
    margin-top: 30px;
  }}
  h3 {{
    color: #444;
    font-size: 16px;
  }}
  .card {{
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    padding: 20px;
    margin: 20px 0;
    background: #fafafa;
  }}
  hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 20px 0;
  }}
  p {{
    line-height: 1.7;
    margin: 8px 0;
  }}
  strong {{
    color: #1a1a2e;
  }}
  ul, ol {{
    padding-left: 20px;
    line-height: 1.8;
  }}
  .footer {{
    margin-top: 30px;
    font-size: 12px;
    color: #999;
    text-align: center;
  }}
</style>
</head>
<body>
<div class="wrapper">
{_markdown_to_html(content)}
<div class="footer">
  Gerado automaticamente pelo sistema TMZ Conect · {date_str}
</div>
</div>
</body>
</html>"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = recipient

    part_text = MIMEText(content, "plain", "utf-8")
    part_html = MIMEText(html_body, "html", "utf-8")
    msg.attach(part_text)
    msg.attach(part_html)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, msg.as_string())

    print("✅ Email enviado com sucesso!")


if __name__ == "__main__":
    try:
        now = datetime.now()
        print(f"🚀 Iniciando geração de conteúdo — {now.strftime('%d/%m/%Y %H:%M:%S')}")

        print("🔍 Pesquisando notícias recentes...")
        news = search_news()
        print(f"📰 {len(news)} artigos encontrados")

        if len(news) == 0:
            print("⚠️  Nenhuma notícia encontrada — o Claude usará seu próprio conhecimento atualizado.")

        print("🤖 Gerando 3 opções de roteiro com Claude...")
        content = generate_content(news)

        print("📧 Enviando email...")
        send_email(content)

        print("✅ Processo concluído com sucesso!")
    except Exception:
        print("❌ Erro durante execução:")
        traceback.print_exc()
