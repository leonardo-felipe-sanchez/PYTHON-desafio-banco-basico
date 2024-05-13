usuario = []

def procurar_cpf(usuario, cpf):
    for idi, tupla_i in enumerate(usuario):
        for idj, tupla_j in enumerate(range(4)):
            if usuario[idi][idj] == cpf:
                return f"o usuario {usuario[idi][idj]} existe, digite novamente"
                break

    return f"usuario novo"
        
def criar_usuario(cliente):
    return cliente

while True:
    cpf = int(input("digite apenas em numeros o CPF: "))
    if procurar_cpf(usuario, cpf) == "usuario novo":
        nome = input("digite o nome: ")
        nascimento = input("digite a data de nascimento: ")
        print("agora nos informe o endereco, se prepare: ")
        logradouro = input("digite o logradouro: ")
        numero = input("digite o numero: ")
        bairro = input("digite o bairro: ")
        cidade = input("digite a cidade: ")
        estado = input("digite a UF do estado: ")
        
        
        #endereco = [logradouro, numero, bairro, cidade, estado]
        #usuario = dict(cpf = cpf, nome = nome, nascimento= nascimento)
        #depositorio = [logradouro, numero, bairro, cidade, estado]
        #endereco.extend(depositorio)
        #depositorio = [cpf, nome, nascimento, endereco]
        usuario.append(criar_usuario([cpf, nome, nascimento,[logradouro, numero, bairro, cidade, estado]]))

            
        print(usuario)
    else:
        print(procurar_cpf(usuario, cpf))