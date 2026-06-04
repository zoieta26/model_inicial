import sys
from view.tela_principal import TelaPrincipal
from controllers.controlador_pessoas import ControladorPessoas
from controllers.controlador_relatorios import ControladorRelatorios
from controllers.controlador_atendimentos import ControladorAtendimentos
from controllers.controlador_clinicas import ControladorClinicas
from dao import DAO  

class ControladorPrincipal:
    def __init__(self):
        self.__tela = TelaPrincipal()
        self.ctrl_clinicas = ControladorClinicas(self)
        self.ctrl_atendimentos = ControladorAtendimentos(self)
        self.ctrl_pessoas = ControladorPessoas(self)
        self.ctrl_relatorios = ControladorRelatorios(self)
        
        self.__dao = DAO()         
        self.carregar_dados()      

    def carregar_dados(self):
        
        dados = self.__dao.carregar()
        
        
        self.ctrl_pessoas.pacientes.extend(dados["pacientes"])
        self.ctrl_pessoas.profissionais.extend(dados["profissionais"])
        self.ctrl_clinicas.get_clinicas().extend(dados["clinicas"])
        self.ctrl_atendimentos.atendimentos.extend(dados["atendimentos"])

    def salvar_dados(self):
        
        dados = {
            "pacientes": self.ctrl_pessoas.pacientes,
            "profissionais": self.ctrl_pessoas.profissionais,
            "clinicas": self.ctrl_clinicas.get_clinicas(),
            "atendimentos": self.ctrl_atendimentos.atendimentos
        }
        self.__dao.salvar(dados)

    def iniciar(self):
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 1:
                self.ctrl_pessoas.abrir_tela()
            elif opcao == 2:
                self.ctrl_clinicas.abrir_tela()
            elif opcao == 3:
                self.ctrl_atendimentos.abrir_tela()
            elif opcao == 4:
                self.ctrl_relatorios.abrir_tela()
            elif opcao == 0:
                self.salvar_dados()
                print("\nA guardar todos os dados com segurança...")
                print("Sistema encerrado com sucesso.")
                sys.exit(0)