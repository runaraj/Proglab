liste = [1,2,3,4,5]

for i in range(1, len(liste)):
    liste[i] = liste[i]+liste[i-1]


print(liste)