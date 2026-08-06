def criar_usuario(**dados):
    print("Novo usuario criado com os dados :", dados)

criar_usuario(nome="Maria", idade=29, cidade="Serra", curso="Computacao")

# ---------------------------------------------
my_list = ["Ola", 2, 78.5, [1, True, "Casa"]]
print(my_list[-2])
my_list[-2] = False
print(my_list)

matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(matrix)

# ---------------------------------------------

#Tupla: imutável e declarada pro parênteses (ou sem parêntese)
#Lista: mutável e declarada co colchetes

tupla_01 = (1, 78.5, ["casa", 87], True, (45, "Maria"))
print(tupla_01)
tupla_01 = (True, 78.5, ["casa", 87], True, (45, "Maria"))
tupla_01[2][1] = False
print(tupla_01)

# ---------------------------------------------


#atribuindo valores de cada posição da tupla à variáveis, mas se alterar o valor da variável não altera o da tupla
tupla_01 = 1, 2, 3
a, b, c = tupla_01
print(a)
a = 30
print(a)

#não é tupla
tupla_01 = (1)

# ---------------------------------------------

#dicionários são declarados por chaves e rótulos, são mutáveis e possuem rótulos, para manter a semântica dos dados
dic_01 = {
    "nome": 'Ana',
    "idade": 25,
    "cidade": 'Serra',
    1: 78.8,
    "dic_int":{
        "saída": 10,
        "entrada": 78
    }
}
print(dic_01["dic_int"]["saída"])
dic_01["dic_int"] = True
print(dic_01["dic_int"])

# ---------------------------------------------

#Conjuntos são delcarados por chaves sem rótulos e permitem operações (motivo de ser diferente das outras)
frutas = {"maca", "banana", "laranja"}
print(frutas)
#adiciona em qualquer lugar do conjunto
frutas.add("uva")
print(frutas)
print("maca" in frutas)

lista_fruta = ["maca", "banana", "laranja"]
print("maca" in lista_fruta)

#operações com conjuntos
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b)
print(a & b)
print(a - b)
print(a ^ b)

# ---------------------------------------------

def pao (func):
    def wrapper(*args, **kwargs):
        print("--- Fatia superior do pão ---")
        resultado = func(*args, **kwargs)
        print("--- Fatia inferior do pão ---")
        return resultado
    return wrapper

@pao # Decorator
def hamburguer_vegano():
    print("Recheio do meu hamburguer")

hamburguer_vegano()
