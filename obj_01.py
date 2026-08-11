#Utilizando Programação Orientada ao Objeto (sem camadas de seurança) para programar

class Produto:
    def __init__(self, codigo: int, descricao: str, preco: float) -> None:
        self.codigo = codigo
        self.descricao = descricao
        self.preco = preco
        self.quantidade_estoque = 0

    def entrada_estoque(self, quantidade: float) -> None:
        self.quantidade_estoque += quantidade

    def saida_estoque(self, quantidade: float) -> None:
            self.quantidade_estoque -= quantidade

    def visualizar_quantidade_estoque(self) -> None:
         print(f"A quantidade do produto {self.descricao} é: {self.quantidade_estoque}")

if __name__ == "__main__":
    print("--- Estoque em POO ---")
    produto_01 = Produto(1, "Notebook", 3500.0)
    produto_01.visualizar_quantidade_estoque()
    produto_01.entrada_estoque(10)
    produto_01.visualizar_quantidade_estoque()
    produto_01.saida_estoque(1)
    produto_01.visualizar_quantidade_estoque()

    produto_01.quantidade_estoque = 200
    produto_01.visualizar_quantidade_estoque()

    #  produto_02 = {"codigo": 2, "descricao": 'Pneu', "quantidade_estoque": 100}
    #  print(produto_02)
