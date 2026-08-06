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
