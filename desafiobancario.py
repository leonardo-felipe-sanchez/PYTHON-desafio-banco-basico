from abc import ABC, abstractmethod
from pathlib import Path
import re
import datetime

class Transacao(ABC):
    @abstractmethod
    def Registrar(self, conta):
        pass


class Historico:
    def __init__(self):
        self._transacoes = []

    def adicinar_transacao(self, transacao):
        self._transacoes.append(transacao)

class Cliente:
    def __init__(self, cpf, nome, data_nascimento):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._contas = []

    def adicionar_conta(self, conta, numero):
        adicionar_conta = ContaCorrente(conta)
        self._contas.append(adicionar_conta)
        self._contas[int(len(self._contas)) - 1].nova_conta(
            [self._cpf, self._nome, self._data_nascimento, self._endereco], numero
        )

    def realizar_transacao(self, transacao, conta=0):
        transacao.Registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco=-1, contas=[]):
        super().__init__(cpf, nome, data_nascimento)
        self._endereco = endereco
        self._contas = contas


def log_decorator(func):
    def wrapper(*args, **kwargs):
        now = datetime.datetime.now()
        with open(log_file, "a", encoding="utf-8") as arquivo:
            arquivo.writelines(f"Data e hora da transação: {now} ")
            arquivo.writelines(f"Tipo da transação: {func.__name__} \n")
        result = func(*args, **kwargs)
        return result
    return wrapper


class Conta:
    def __init__(self, saldo, numero=0, cliente=0, agencia=1, historico=Historico()):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    def Saldo(self, saldo):
        self._saldo = saldo

    @log_decorator
    def nova_conta(self, cliente, numero):
        self._cliente = PessoaFisica(cliente[0], cliente[1], cliente[2], cliente[3])
        self._numero += numero

    def sacar(self, valor):
        saldo = -int(valor) + int(self._saldo)
        self.Saldo(saldo)
        return True

    def depositar(self, valor):
        saldo = int(self._saldo) + int(valor)
        self.Saldo(saldo)
        return True

    def __str__(self) -> str:
        return f"{self._numero}"


class ContaCorrente(Conta):
    def __init__(self, saldo, numero=0, cliente=0, agencia=1, historico=Historico(), limite=0, limite_saques=10):
        super().__init__(saldo, numero, cliente, agencia, historico)
        self._limite = limite
        self._limite_saques = limite_saques


@log_decorator
class Deposito(Transacao):
    def __init__(self, valor=0):
        self._valor = valor

    def Registrar(self, conta):
        conta[0][conta[1]]._contas[conta[2]].depositar(conta[3])
        conta[0][conta[1]]._contas[conta[2]]._historico.adicinar_transacao(
            f"{conta[0][conta[1]]._contas[conta[2]]._cliente}, "
            f"{conta[0][conta[1]]._cpf}, "
            f"{conta[4]} + {conta[3]} = "
            f"{conta[0][conta[1]]._contas[conta[2]]._saldo}, "
            f"{datetime.datetime.now()}"
        )


@log_decorator
class Saque(Transacao):
    def __init__(self, valor=0):
        self._valor = valor

    def Registrar(self, conta):
        conta[0][conta[1]]._contas[conta[2]].sacar(conta[3])
        conta[0][conta[1]]._contas[conta[2]]._historico.adicinar_transacao(
            f"{conta[0][conta[1]]._contas[conta[2]]._cliente}, "
            f"{conta[0][conta[1]]._cpf}, "
            f"{conta[4]} - {conta[3]} = "
            f"{conta[0][conta[1]]._contas[conta[2]]._saldo}, "
            f"{datetime.datetime.now()}"
        )


def formatarData(data_nascimento):
    if re.findall(r"[^a-zA-Z0-9\s]", data_nascimento) or re.findall(
        r'[^\S\n\t]+', data_nascimento
    ):
        if data_nascimento.find(" "):
            data_nascimento = data_nascimento.replace(" ", "-")
        data_nascimento = re.split(r"[^a-zA-Z0-9\s]", data_nascimento)
    else:
        result = ""
        for index, character in enumerate(data_nascimento):
            if index == 1 or index == 3:
                result = result + character + " "
            else:
                result = result + character
        data_nascimento = result.split()
    return datetime.datetime(
        int(data_nascimento[2]), int(data_nascimento[1]), int(data_nascimento[0])
    )


def verificar_cpf(classeLista, cpf):
    resultado = "usuario novo"
    for index, classes in enumerate(classeLista, 0):
        if int(cpf) == int(classes._cpf):
            resultado = index
    return resultado


menu, menu2 = (
    """
menu banco
digite 1 para o saque
digite 2 para o deposito
digite 3 para o extrato
digite 4 para sair
""",
    """
menu
digite 1 para o cadastro
digite 2 para criar o banco
digite 3 para acessar o banco
digite 4 para sair
""",
)
opcao, escolha, looping, laco, index, index2, numero_conta = (
    0,
    0,
    True,
    True,
    -1,
    0,
    0,
)
classeLista = []
ROOT_PATH = Path(__file__).parent
log_file = ROOT_PATH / "registro.log"

while True:
    opcao = int(input(menu2))
    if opcao == 1:
        while looping is True:
            cpf = input("digite o cpf: ")
            cpf = [digit for digit in cpf if digit.isdigit()]
            cpf = "".join(cpf)
            cpf = int(cpf)
            if verificar_cpf(classeLista, cpf) == "usuario novo" or verificar_cpf(
                classeLista, cpf
            ) is None:
                nome = input("digite o nome: ")
                data_nascimento = input("digite a data de nascimeno: ")
                data_nascimento = formatarData(data_nascimento)
                endereco = input("digite o logradouro: ")
                endereco = endereco + " " + input("digite o numero: ")
                endereco = endereco + " " + input("digite o bairro: ")
                endereco = endereco + " " + input("digite a cidade: ")
                endereco = endereco + " " + input("digite a UF do estado: ")
                classeLista.append(PessoaFisica(cpf, nome, data_nascimento, endereco))
                encerra = input("Deseja criar um novo usuario?")
                if encerra.lower() in ("sim", "s"):
                    continue
                elif encerra.lower() in ("nao", "n"):
                    looping = False
                    break
                else:
                    print("opcao invalida, logo tu escolheu não, bye bye")
                    break
            else:
                print("usuario existe, retornando ao menu ...")
                break

    elif opcao == 2:
        valor_cpf = input("digite o CPF")
        valor_cpf = [digit for digit in valor_cpf if digit.isdigit()]
        valor_cpf = "".join(valor_cpf)
        valor_cpf = int(valor_cpf)
        index = 0
        for classes in classeLista:
            numero_conta += 1
            if int(valor_cpf) == int(classes._cpf):
                classeLista[index].adicionar_conta(0, numero_conta)
                print(
                    f"prezado {classeLista[index]._nome} sua conta "
                    f"{classeLista[index]._contas[int(len(classeLista[index]._contas)) - 1]._numero} "
                    f"foi criada"
                )
                break
            else:
                print("procurando")
            index += 1
        valor_cpf = 0

    elif opcao == 3:
        acesso = input("digite o CPF")
        acesso = [digit for digit in acesso if digit.isdigit()]
        acesso = "".join(acesso)
        acesso = int(acesso)
        index = verificar_cpf(classeLista, acesso)
        numero_acesso_conta = -1
        index2 = 0
        if verificar_cpf(classeLista, acesso) != "usuario novo":
            acesso_conta = int(input("digite a conta de acesso: "))
            for count, numeros in enumerate(classeLista[index]._contas, 0):
                if int(numeros._numero) == int(acesso_conta):
                    numero_acesso_conta = count
                    break
            if numero_acesso_conta != -1:
                print(
                    f"conta {classeLista[index]._contas[numero_acesso_conta]._numero} acessada"
                )
                while laco is True:
                    escolha = int(input(menu))
                    if escolha == 1:
                        if int(
                            classeLista[index]._contas[numero_acesso_conta]._limite
                        ) != int(
                            classeLista[index]._contas[numero_acesso_conta]._limite_saques
                        ):
                            dinheiro = int(input("digite o valor a ser sacado: "))
                            saldo = classeLista[index]._contas[numero_acesso_conta]._saldo
                            if dinheiro < 0:
                                print("valor invalido")
                            elif dinheiro > saldo:
                                print("saque maior que saldo")
                            else:
                                classeLista[index]._contas[
                                    numero_acesso_conta
                                ]._limite += 1
                                saque = Saque(dinheiro)
                                classeLista[index].realizar_transacao(
                                    saque,
                                    [
                                        classeLista,
                                        index,
                                        numero_acesso_conta,
                                        dinheiro,
                                        saldo,
                                    ],
                                )
                                print("saque realizado com sucesso")
                        else:
                            print("limite de saque atingido")

                    elif escolha == 2:
                        dinheiro = int(input("digite o valor a ser depositado: "))
                        saldo = classeLista[index]._contas[numero_acesso_conta]._saldo
                        if dinheiro > 0:
                            deposito = Deposito(dinheiro)
                            classeLista[index].realizar_transacao(
                                deposito,
                                [
                                    classeLista,
                                    index,
                                    numero_acesso_conta,
                                    dinheiro,
                                    saldo,
                                ],
                            )
                            print("deposito realizado com sucesso")
                        else:
                            print("valor invalido")

                    elif escolha == 3:
                        split_list = [
                            item.split(", ")
                            for item in classeLista[index]._contas[
                                numero_acesso_conta
                            ]._historico._transacoes
                        ]
                        for historicidade in split_list:
                            if str(historicidade[0]) == str(
                                classeLista[index]._contas[numero_acesso_conta]._cliente
                            ):
                                print(f"{historicidade[3]} - {historicidade[2]}")

                    elif escolha == 4:
                        laco = False
                        break
                laco = True
        else:
            print("conta nao existe")

    elif opcao == 4:
        break
    opcao = 0
    looping = True