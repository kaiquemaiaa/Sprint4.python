from datetime import datetime
import json

class EstacionamentoException(Exception):
    pass

class QuantidadeInvalidaException(EstacionamentoException):
    def __init__(self, message="Quantidade inválida. Deve ser um número inteiro maior que zero."):
        super().__init__(message)

class VagasInsuficientesException(EstacionamentoException):
    def __init__(self, message="Não há vagas suficientes para adicionar tantos carros."):
        super().__init__(message)

class CarrosInsuficientesException(EstacionamentoException):
    def __init__(self, message="Não há carros suficientes no estacionamento."):
        super().__init__(message)

class Estacionamento:
    def __init__(self):
        self.carros = 0
        self.vagas_totais = 150
        self.vagas_disponiveis = self.vagas_totais
        self.transacoes = []

    def adicionar_carro(self, quantidade):
        try:
            self.validar_quantidade(quantidade)
            if self.vagas_disponiveis < quantidade:
                raise VagasInsuficientesException(f"Apenas {self.vagas_disponiveis} vagas disponíveis. Não é possível adicionar {quantidade} carros.")
            self.carros += quantidade
            self.vagas_disponiveis -= quantidade
            self.registrar_transacao("adicionados", quantidade)
        except QuantidadeInvalidaException as e:
            print(f"Erro ao adicionar carros: {e}")
        except VagasInsuficientesException as e:
            print(f"Erro ao adicionar carros: {e}")

    def retirar_carro(self, quantidade):
        try:
            self.validar_quantidade(quantidade)
            if self.carros < quantidade:
                raise CarrosInsuficientesException(f"Apenas {self.carros} carros no estacionamento. Não é possível retirar {quantidade} carros.")
            self.carros -= quantidade
            self.vagas_disponiveis += quantidade
            self.registrar_transacao("retirados", quantidade)
        except QuantidadeInvalidaException as e:
            print(f"Erro ao retirar carros: {e}")
        except CarrosInsuficientesException as e:
            print(f"Erro ao retirar carros: {e}")

    def mostrar_transacoes(self):
        print("\nRegistro de Transações:")
        for transacao in self.transacoes:
            print(f"{transacao['Data/Hora']} - {transacao['Mensagem']}")

    def validar_quantidade(self, quantidade):
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise QuantidadeInvalidaException()

    def registrar_transacao(self, tipo, quantidade):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mensagem = f"{quantidade} carros {tipo} ao estacionamento."
        transacao = {"Data/Hora": data_hora, "Mensagem": mensagem}
        self.transacoes.append(transacao)

def mostrar_informacoes_json():
    try:
        with open('informacoes.json', 'r') as arquivo_json:
            informacoes = json.load(arquivo_json)
            print("\nInformações do Estacionamento:\n")
            print(f"{informacoes['nome_estacionamento']}")
            print(f"Endereço: {informacoes['endereco']}\n")
            print("Contato:")
            print(f" Telefone: {informacoes['contato']['telefone']}")
            print(f" Email: {informacoes['contato']['email']}")
    except FileNotFoundError:
        print("\nArquivo 'informacoes.json' não encontrado.")
    except json.JSONDecodeError:
        print("\nErro ao decodificar o arquivo JSON.")

def menu():
    print("\n=============== Menu ===============")
    print("1 - Adicionar Carros")
    print("2 - Retirar Carros")
    print("3 - Mostrar Transações")
    print("4 - Mostrar Informações do Estacionamento (JSON)")
    print("5 - Sair")
    print(f"Vagas disponíveis: {estacionamento.vagas_disponiveis}/{estacionamento.vagas_totais}")

def escolher_opcao():
    while True:
        try:
            opcao = int(input("\nEscolha uma opção: "))
            if 1 <= opcao <= 5:
                return opcao
            else:
                print("Opção inválida. Escolha novamente.")
        except ValueError:
            print("Por favor, insira um número inteiro válido.")

estacionamento = Estacionamento()

while True:
    menu()
    opcao = escolher_opcao()

    if opcao == 1:
        while True:
            try:
                quantidade = int(input("\nDigite a quantidade de carros a ser adicionada: "))
                estacionamento.adicionar_carro(quantidade)
                break
            except EstacionamentoException as e:
                print(f"Erro: {e}")
                break  # Adicionado para sair do loop e voltar ao menu após exibir a mensagem de erro
    elif opcao == 2:
        while True:
            try:
                quantidade = int(input("\nDigite a quantidade de carros a serem retirados: "))
                estacionamento.retirar_carro(quantidade)
                break
            except EstacionamentoException as e:
                print(f"Erro: {e}")
                break  # Adicionado para sair do loop e voltar ao menu após exibir a mensagem de erro
    elif opcao == 3:
        estacionamento.mostrar_transacoes()
    elif opcao == 4:
        mostrar_informacoes_json()
    elif opcao == 5:
        print("\nSaindo do programa.")
        break
    else:
        print("\nOpção inválida. Escolha novamente.")
