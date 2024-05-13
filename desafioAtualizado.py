menu, menu2 = ('''
menu banco
digite 1 para o saque
digite 2 para o deposito
digite 3 para o extrato
digite 4 para sair
''',
'''
menu
digite 1 para o cadastro
digite 2 para criar o banco
digite 3 para acessar o banco
digite 4 para sair
'''
)
saldo, saldo_comparativo = (0,0)
extrato, usuario, conta = ([],[], [])
limite, acesso, valor, numero_da_conta = (3, 0, 0, 0)
looping = True

def procurar_cpf(usuario, cpf):
    for idi, tupla_i in enumerate(usuario):
        for idj, tupla_j in enumerate(range(4)):
            if usuario[idi][idj] == cpf:
                return f"o usuario {usuario[idi][idj]} existe, digite novamente"
                break

    return f"usuario novo"

def criar_usuario(usuario, cliente):
    usuario.append(cliente)
    return cliente

def criar_conta(funcao, valor_cpf, usuario, numero_da_conta):
   resultado = funcao(usuario, valor_cpf)
   if resultado != "usuario novo":
      numero_da_conta += 1
      return numero_da_conta
   else:
      return 0

def inserir_extrato(saldo, saldo_comparativo,/,*, valor):
   if saldo > saldo_comparativo:
      return f"+{valor}: {saldo}"
   else:
      return f"-{valor}: {saldo}"

def verificar_limite(limite, acesso):
   if acesso == limite:
      return False
   else:
      acesso += 1
      return acesso

def sacar(*, valor, saldo):
   if valor > saldo:
      return saldo
   else:
      return -valor + saldo

def depositar(valor, saldo, /):
      return valor + saldo

while True:
   looping = True
   escolha = int(input(menu2))
   if escolha == 1:
      while looping == True:
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
            criar_usuario(usuario,[cpf, nome, nascimento,[logradouro, numero, bairro, cidade, estado]])
            print(usuario)
            encerra = input("Deseja criar um novo usuario?")
            if encerra == "sim" or encerra == "SIM" or encerra=="Sim" or encerra == "s" or encerra == "s":
               continue
            elif encerra == "nao" or encerra == "NAO" or encerra=="Nao" or encerra == "N" or encerra == "n":
               looping = False
               break
            else:
               print("opcao invalida, logo tu escolheu sim, bye bye")
         else:
            print(procurar_cpf(usuario, cpf))
   elif escolha == 3:
      while True:
         opcao = int(input(menu)) 
         if opcao ==1:
            acesso = verificar_limite(limite, acesso)
            if acesso == False:
               print("limite de saque atingido")
            else:
               valor = float(input("digite o valor do saldo"))
               if valor > 0:
                  saldo_comparativo = saldo
                  saldo = sacar(valor = valor, saldo =saldo)
                  if saldo == saldo_comparativo:
                     print("erro: saque maior que o saldo")
                  else:
                     extrato.append(f"{inserir_extrato(saldo, saldo_comparativo, valor = valor)}")
               else:
                  print("valor invalido")
      
         elif opcao ==2:
            valor = float(input("digite o valor do deposito "))
            if valor > 0:
               saldo_comparativo = saldo
               saldo = depositar(valor,saldo)
               extrato.append(f"{inserir_extrato(saldo, saldo_comparativo, valor = valor)}")
            else:
               print("valor invalido")  
         elif opcao ==3:
            for exibir in extrato:
               print(exibir)
         elif opcao == 4:
            break
         else:
            print("numero invalido, tente novamente")
         valor = 0
         saldo_comparativo = 0
   elif escolha == 2:
      valor_cpf= int(input("digite o CPF"))
      validacao = criar_conta(procurar_cpf, valor_cpf, usuario, numero_da_conta)
      if validacao == 0:
         print("Usuario nao existe, nao sera possivel criar conta")
      else:
         numero_da_conta = validacao
         conta.append([valor_cpf, 1, numero_da_conta])
         print(f"conta {numero_da_conta} da agencia 1 criada")

   elif escolha == 4:
      break