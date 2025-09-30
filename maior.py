# Descobrir maior numero entre 3

numero1 = int(input('Digite o primeiro numero'))
numero2 = int(input('Digite o segundo numero'))
numero3 = int(input('Digite o terceiro numero'))

if numero1 >= numero2 and numero1 >= numero3:
    print('O ', numero1, ' é maior')
elif numero2 >= numero3:
    print('O ', numero2, ' é maior')
else:
    print('O ', numero3, ' é maior')

