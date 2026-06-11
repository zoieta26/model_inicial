import sys
from view.tela_principal import TelaPrincipal
from controllers.controlador_pessoas import ControladorPessoas
from controllers.controlador_relatorios import ControladorRelatorios
from controllers.controlador_atendimentos import ControladorAtendimentos
from controllers.controlador_clinicas import ControladorClinicas

class ControladorPrincipal:
    def __init__(self):
        self.__tela = TelaPrincipal()
        self.ctrl_clinicas = ControladorClinicas(self)
        self.ctrl_atendimentos = ControladorAtendimentos(self)
        self.ctrl_pessoas = ControladorPessoas(self)
        self.ctrl_relatorios = ControladorRelatorios(self)

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
                print("Encerrando o sistema...")
                sys.exit(0)