import FreeSimpleGUI as sg
from view.tela_generica import TelaGenerica

class TelaPrincipal(TelaGenerica):
    def __init__(self):
        super().__init__()
        self.init_components()

    def init_components(self):
        layout = [
            [sg.Text("SISTEMA DE CLÍNICAS", font=("Helvetica", 22))],
            [sg.Button("Módulo Pessoas", size=(28, 1))],
            [sg.Button("Módulo Clínicas", size=(28, 1))],
            [sg.Button("Módulo Atendimentos", size=(28, 1))],
            [sg.Button("Módulo Relatórios", size=(28, 1))],
            [sg.Button("Módulo Tipos de Atendimento", size=(28, 1))],
            [sg.Button("Sair", size=(28, 1))]
        ]
        self._criar_janela("Sistema de Clínicas", layout)

    def tela_opcoes(self) -> str:
        self.init_components()  # janela não pode ser reaberta depois de fechada
        evento, _ = self.open()
        self.close()

        return "Sair" if evento == sg.WIN_CLOSED else evento
