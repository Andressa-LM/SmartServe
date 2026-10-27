"""Executa uma demonstração de atendimento pelo terminal."""

# O terminal reutiliza catálogo e regras do backend para evitar duplicação.
# Assim, recomendações e validações permanecem consistentes entre as interfaces.
from app import (
    construir_prompt_inteligente,
    recomendar_produtos,
    simular_resposta,
)


def executar_atendimento():
    """Solicita dados e exibe recomendações da API ou do catálogo local."""
    print("=== SmartServeAI | Atendimento local ===")
    nome = input("Como podemos chamar você? ").strip()
    interesse = input("Qual é o seu interesse? ").strip()
    mensagem = input("Como podemos ajudar? ").strip()

    # Repete no terminal as validações básicas usadas no formulário web.
    if not nome or not interesse or not mensagem:
        raise ValueError("Nome, interesse e mensagem são obrigatórios.")
    if len(nome) > 80 or len(mensagem) > 1000:
        raise ValueError("Nome ou mensagem excede o limite permitido.")

    recomendacoes = recomendar_produtos(interesse)
    resposta = simular_resposta(nome, mensagem, recomendacoes)
    prompt = construir_prompt_inteligente(nome, mensagem, recomendacoes)

    print("\n--- Resposta ---")
    print(resposta)
    print("\n--- Produtos recomendados ---")
    if recomendacoes:
        for produto in recomendacoes:
            print(f"- {produto['nome']} | R$ {produto['preco']:.2f}")
            print(f"  Ver no Mercado Livre: {produto['permalink']}")
    else:
        print("Nenhum produto encontrado para esse interesse.")
    print("\n--- Prompt estruturado ---")
    print(prompt)


def main():
    """Executa a demonstração e informa dados inválidos sem ocultar o erro."""
    try:
        executar_atendimento()
    except ValueError as erro:
        print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
