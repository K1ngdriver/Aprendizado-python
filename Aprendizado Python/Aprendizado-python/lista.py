# Lista de compras inteligente
'''compras = []

print("=== LISTA DE COMPRAS ===")
print("Digite os itens (digite 'fim' para terminar)")
print("Digite *lista* para ver os itens que tem na sua lista de compras!")
print("Digite *tamanho* para saber o tamanho de sua lista")

while True:  # Loop infinito até alguém digitar 'fim'
    item = input("Item: ")
    
    compras.append(item)
    
    if item == "lista":
        print(compras)
    if item == "tamanho":
        print(len(compras))
    if item == "":
        print('Você precisa digitar algum item ou digitar fim para finalizar o código')
    if item == "fim":
        break  # Para o loop
    
    # Aqui você adiciona o item na lista
    # E depois mostra quantos itens já tem

# Aqui você vai usar while, input, append e if
# Tente fazer sozinho primeiro!'''


# Código da Claudeai
compras = []
print("=== LISTA DE COMPRAS ===")
print("Digite os itens (digite 'fim' para terminar)")
print("Comandos: 'lista' para ver itens, 'tamanho' para contar")
print("Digite 'remover' para retirar um item da lista")

while True:
    item = input("Item: ")
    
    # PRIMEIRO verificamos os comandos especiais
    if item == "fim":
        break
    elif item == "lista":
        print(f"Seus itens: {compras}")
        continue  # Volta para o início do loop SEM adicionar na lista
    elif item == "tamanho":
        print(f"Você tem {len(compras)} itens")
        continue  # Volta para o início do loop SEM adicionar na lista
    # Se o usuário digitar "remover", pergunte qual item tirar
    elif item == "remover":
        if len(compras) == 0:
            print("Lista vazia!")
        else:
            print(f"Itens disponíveis: {compras}")
            remover = input("Qual item remover? ")
            
            try:
                compras.remove(remover)
                print(f"'{remover}' removido com sucesso!")
            except ValueError:
                print(f"'{remover}' não está na lista!")
        # Aqui você tenta remover (dica: use try/except ou if/in)
    elif item == "":
        print("Você precisa digitar algum item!")
        continue  # Volta para o início do loop SEM adicionar na lista
    else:
        # SÓ AQUI adicionamos itens reais
        compras.append(item)
        print(f"'{item}' adicionado! Total: {len(compras)} itens")

print(f"\n🛒 Lista final: {compras}")