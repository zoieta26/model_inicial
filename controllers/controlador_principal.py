import sys
from view.tela_principal import TelaPrincipal
from controllers.controlador_pessoas import ControladorPessoas
from controllers.controlador_relatorios import ControladorRelatorios
from controllers.controlador_atendimentos import ControladorAtendimentos
from controllers.controlador_clinicas import ControladorClinicas
from controllers.controlador_tipos_atendimento import ControladorTiposAtendimento

class ControladorPrincipal:
    __instance = None  # instância única (padrão Singleton)

    def __init__(self):
        self.__tela = TelaPrincipal()


        self.ctrl_clinicas = ControladorClinicas(self)
        self.ctrl_pessoas = ControladorPessoas(self)
        self.ctrl_tipos_atendimento = ControladorTiposAtendimento(self)
        self.ctrl_atendimentos = ControladorAtendimentos(self)
        self.ctrl_relatorios = ControladorRelatorios(self)

    def __new__(cls):
        if ControladorPrincipal.__instance is None:
            ControladorPrincipal.__instance = object.__new__(cls)
        return ControladorPrincipal.__instance

    def iniciar(self):
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == "Módulo Pessoas":
                self.ctrl_pessoas.abrir_tela()
            elif opcao == "Módulo Clínicas":
                self.ctrl_clinicas.abrir_tela()
            elif opcao == "Módulo Atendimentos":
                self.ctrl_atendimentos.abrir_tela()
            elif opcao == "Módulo Relatórios":
                self.ctrl_relatorios.abrir_tela()
            elif opcao == "Módulo Tipos de Atendimento":
                self.ctrl_tipos_atendimento.abrir_tela()
            elif opcao == "Sair":
                print("\nSistema encerrado com sucesso.")
                sys.exit(0)
