doces = [['Doce de Leite', 10],
         ['Brigadeiro', 8],
         ['Pudim', 0],
         ['Banoffe', 0],
         ['Torta de Limão', 7],
         ['Paçoca', 0]]

for doce in doces:
    if doce[1] > 5:
        print(doce[0])