x = int(input("Please enter an integer: "))

if x < 0:
    x = 0
    print('Negative changed to zero')
elif x == 0:
    print('Zero')
elif x == 1:
    print('Single')
else:
    print('More')

#While em python
# Contagem regressiva:
contador = 5
while contador > 0:
    print(contador)
    contador -= 1

#For em python
# Mede algumas strings:
palavras = ['gato', 'janela', 'defenestrar']
for p in palavras:
    print(p, len(p))

# Cria uma amostra de coleção
users = {'Hans': 'active', 'Éléonore': 'inactive', '景太郎': 'active'}

# Estratégia: iterar por uma cópia
for user, status in users.copy().items():
    if status == 'inactive':
        del users[user]

# Estratégia: criar uma nova coleção
active_users = {}
for user, status in users.items():
    if status == 'active':
        active_users[user] = status

#Range em python
for i in range(5):
    print(i)

list(range(5, 10))


list(range(0, 10, 3))


list(range(-10, -100, -30))

a = ['Maria', 'tinha', 'um', 'carneirinho']
for i in range(len(a)):
    print(i, a[i])