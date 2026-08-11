class Produto:
    def __init__(self, codigo: int, descricao: str, preco: float) -> None:
        # A inicializacao usa internamente as properties para garantir validacao
        self.__codigo = codigo
        self.__descricao = descricao
        self.preco = preco #Chama o setter automaticamente
        self.__quantidade_estoque = 0

    def entrada_estoque(self, quantidade: float) -> None:
        self.__quantidade_estoque += quantidade

    def saida_estoque(self, quantidade: float) -> None:
        self.__quantidade_estoque -= quantidade

    def visualizar_quantidade_estoque(self) -> None:
        print(f"A quantidade em estoque e {self.__quantidade_estoque}")

    @property
    def codigo(self) -> int:
        """Getter: Permite apenas leitura do codigo"""
        return self.__codigo

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        """Setter: Permite alterar a descricao com controle"""
        self.__descricao = descricao

    @property
    def preco(self) -> float:
        return self.__preco

    @preco.setter
    def preco(self, preco: float) -> None:
        """Setter: Garante que o preco nunca seja zero ou negativo"""
        if preco <= 0:
            raise ValueError("O preco deve ser um valor positivo")
        self.__preco = preco

    @property
    def quantidade_estoque(self) -> float:
        return self.__quantidade_estoque

# Teste de robustez do sistema
if __name__ == "__main__":
    print("--- Testando Encapsulamento com @property ---")

    p1 = Produto(1, "Notebook", 3500.0)

    # Acesso sintatico de atributo, mas execucao de metodo (Getter)
    print(f"Produto: {p1.descricao} | Preco: R$ {p1.preco}")

    print(f"\n--- Testando Alteracao com Validacao (Setters) ---")
    p1.descricao = "Notebook Gamer" # Funciona normalmente
    p1.preco = 4200.0 # Funciona normalmente

    try:
        print("Tentando definir preco invalido: -100...")
        p1.preco = -100
    except ValueError as e:
        print(f"BLOQUEIO DE SEGURANÇA: {e}")

    print("\n--- Verificando Atributos Somente-Leitura ---")
    try:
        # p1.codigo nao possui um @codigo.setter definido
        p1.codigo = 999
    except AttributeError:
        print("ERRO: O código do produto é somente leitura (imune a alterações)")
