menu = '''
menu
digite 1 para o saque
digite 2 para o deposito
digite 3 para o extrato
digite 4 para sair
'''
saldo = 0
valor = 0
extrato = []
limite, acesso = (3, 0)
while True:
    opcao = int(input(menu)) 
    if opcao ==1:
      if acesso < limite:
         acesso += 1
         valor = float(input("digite o valor do saque "))
         if valor > 0:
            if valor > saldo:
                print("saldo insuficiente")
            else:
                saldo -= valor
                extrato.append(f" -{valor}: {saldo}")  
         else:
            print("valor invalido")
      else:
        print("limite de saldo atingido")   
    elif opcao ==2:
      valor = float(input("digite o valor do deposito "))
      if valor > 0:
         saldo += valor
         extrato.append(f" +{valor}: {saldo}")
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
    