#Utilizando POO (com camadas de segurança) para programar

class Produto:
    def __init__(self, codigo: int, descricao: str, preco: float) -> None:
        self.__codigo = codigo
        self.__descricao = descricao
        self.__preco = preco
        self.__quantidade_estoque = 0

    def entrada_estoque(self, quantidade: int) -> None:
        self.__quantidade_estoque += quantidade

    def visualizar_quantidade_estoque(self) -> None:
        print(f"A quantidade do produto {self.__descricao} é: {self.__quantidade_estoque}")

if __name__ == "__main__":
    produto_01 = Produto(1, 'Notebook', 3500.0)
    produto_01.visualizar_quantidade_estoque()
    produto_01.entrada_estoque(10)
    produto_01.visualizar_quantidade_estoque()
    produto_01.__quantidade_estoque = 20
    produto_01.visualizar_quantidade_estoque()
