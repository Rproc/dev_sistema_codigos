# Passagem por Valor
def levelUp(idade):
    idade += 1
    # O += é a mesma coisa que escrever
    # raphael = raphael + 1
    print('Idade atual:', idade)

def levelDown(idade):
    idade = idade - 1
    # Mesma coisa de idade -= 1
    return idade

idade = 10
levelUp(idade)
print('Idade depois da levelUp:', idade)
# necessario que receba o valor do "return" na linha 11
# se não tiver a variavel (a esquerda do igual)
# voce perderá o valor
idade = levelDown(idade)
print('Idade depois da levelDown:', idade)
