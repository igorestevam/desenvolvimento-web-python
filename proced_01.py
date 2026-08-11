# Utilizando a forma de procedures para programar

def cria_produto(codigo: int, descricao: str, preco: float, quantidade_estoque: float) -> dict:
    return {
        "codigo": codigo,
        "descricao": descricao,
        "preco": preco,
        "quantidade_estoque": quantidade_estoque
    }

def entrada_estoque(produto: dict, quantidade: float) -> None:
    produto["quantidade_estoque"] += quantidade

def saida_estoque(produto: dict, quantidade: float) -> None:
    produto["quantidade_estoque"] -= quantidade

def visualizar_quantidade_em_estoque(produto: dict) -> None:
    print(f"A quantidade do produto {produto["descricao"]} é: {produto["quantidade_estoque"]}.")

if __name__ == "__main__":
    print("--- Executando script principal ---")

    produto_01 = cria_produto(1, 'Notebook', 3500.0, 10)
    visualizar_quantidade_em_estoque(produto_01)

    entrada_estoque(produto_01, 15)
    visualizar_quantidade_em_estoque(produto_01)
    saida_estoque(produto_01, 1)
    visualizar_quantidade_em_estoque(produto_01)

    produto_02 = {"codigo": 2, "descricao": 'Pneu', "quantidade_estoque": 3}
    print(produto_02)
    visualizar_quantidade_em_estoque(produto_02)
