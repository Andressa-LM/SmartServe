import unicodedata
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
# Catálogo local usado somente quando a consulta externa falha.
CATALOGO_PRODUTOS = [
    {"id": "local-1", "nome": "Notebook Pro 15", "categoria": "tecnologia", "preco": 4500.0, "tags": ["trabalho", "home office", "tecnologia", "programacao", "ergonomia"]},
    {"id": "local-2", "nome": "Fone Bluetooth", "categoria": "audio", "preco": 350.0, "tags": ["musica", "audio", "trabalho"]},
    {"id": "local-3", "nome": "Livro de Python", "categoria": "livros", "preco": 75.0, "tags": ["estudos", "leitura", "programacao"]},
]
MAPEAMENTO_TERMOS = {
    "trabalho": "notebook mesa cadeira ergonomica escritorio",
    "home office": "notebook suporte cadeira escritorio",
    "programacao": "notebook monitor teclado mecanico programacao",
    "tecnologia": "notebook monitor periféricos pc",
    "estudos": "livro ciencia de dados luminaria mesa caderno",
    "leitura": "livro suporte leitura kindle",
    "musica": "fone de ouvido bluetooth noise cancelling",
    "audio": "fone de ouvido headset microfone",
    "conforto": "cadeira ergonomica apoio pes escritorio",
    "ergonomia": "suporte notebook suporte articulado apoio pes",
}

def recomendar_produtos(interesse):
    """Resolve sinônimos, consulta o Mercado Livre e mantém fallback local."""
    termo = interesse.strip().casefold()
    termo = "".join(c for c in unicodedata.normalize("NFD", termo) if unicodedata.category(c) != "Mn")
    busca = MAPEAMENTO_TERMOS.get(termo) or next(
        (valor for chave, valor in MAPEAMENTO_TERMOS.items()
         if chave in termo or any(palavra in valor.casefold().replace("é", "e").split() for palavra in termo.split())),
        termo,
    )
    try:
        resposta = requests.get("https://api.mercadolibre.com/sites/MLB/search", params={"q": busca}, timeout=5)
        resposta.raise_for_status()
        resultados = resposta.json().get("results", [])
        return [
            {"id": item["id"], "nome": item["title"], "preco": item["price"], "permalink": item["permalink"], "categoria": item.get("category_id", "geral")}
            for item in resultados[:3] if all(item.get(chave) for chave in ("id", "title", "permalink"))]
    except (requests.RequestException, ValueError, TypeError, AttributeError):
        # A indisponibilidade da rede não impede a conclusão do atendimento.
        return [
            {"id": item["id"], "nome": item["nome"], "preco": item["preco"], "permalink": f"https://lista.mercadolivre.com.br/{busca.replace(' ', '-')}", "categoria": item["categoria"]}
            for item in CATALOGO_PRODUTOS if any(tag in item["tags"] for tag in (termo, *termo.split()))][:3]
def construir_prompt_inteligente(nome, mensagem, recomendacoes):
    """Prepara instruções e contexto de produtos para o assistente."""
    nomes = ", ".join(item["nome"] for item in recomendacoes) or "Nenhum produto encontrado"
    return (f"SISTEMA: Você é o SmartServeAI, assistente cortês.\nCLIENTE: {nome}\n"
            f"MENSAGEM: {mensagem}\nPRODUTOS: {nomes}\nResponda com empatia.")
def simular_resposta(nome, mensagem, recomendacoes):
    """Gera resposta local; aqui pode ser conectada uma API de IA externa."""
    saudacao = f"Olá, {nome}! Recebemos sua mensagem: '{mensagem}'."
    nomes = ", ".join(item["nome"] for item in recomendacoes)
    return f"{saudacao} Recomendamos: {nomes}." if nomes else f"{saudacao} Não encontramos produtos."
def processar_atendimento(nome, interesse, mensagem):
    """Orquestra consulta ao catálogo, prompt e resposta do atendimento."""
    produtos = recomendar_produtos(interesse)
    prompt = construir_prompt_inteligente(nome, mensagem, produtos)
    return {"resposta": simular_resposta(nome, mensagem, produtos), "produtos": produtos, "prompt": prompt}
@app.get("/")
def pagina_inicial():
    """Entrega a interface web do atendimento."""
    return render_template("index.html")
@app.post("/api/atendimento")
def atendimento():
    """Valida a requisição REST e responde com JSON."""
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie os dados do formulário em JSON."}), 400
    nome, interesse, mensagem = (dados.get(campo) for campo in ("nome", "interesse", "mensagem"))
    if not all(isinstance(valor, str) and valor.strip() for valor in (nome, interesse, mensagem)):
        return jsonify({"erro": "Preencha nome, interesse e mensagem."}), 400
    if len(nome.strip()) > 80 or len(mensagem.strip()) > 1000:
        return jsonify({"erro": "Nome ou mensagem excede o limite permitido."}), 400
    resultado = processar_atendimento(nome.strip(), interesse.strip(), mensagem.strip())
    return jsonify(resultado)
if __name__ == "__main__":
    app.run(debug=True)
