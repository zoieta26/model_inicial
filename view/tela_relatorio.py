import FreeSimpleGUI as sg
from view.tela_generica import TelaGenerica

class TelaRelatorio(TelaGenerica):
    def __init__(self):
        super().__init__()
        self.init_components()

    def init_components(self):
        layout = [
            [sg.Text("MÓDULO RELATÓRIOS", font=("Helvetica", 18))],
            [sg.Button("Clínicas com mais atendimentos", size=(32, 1))],
            [sg.Button("Relatório Financeiro (Faturação por Clínica)", size=(32, 1))],
            [sg.Button("Procedimentos mais realizados", size=(32, 1))],
            [sg.Button("Atendimentos mais caros e mais baratos", size=(32, 1))],
            [sg.Button("Procedimentos mais caros e mais baratos", size=(32, 1))],
            [sg.Button("Voltar", size=(32, 1))]
        ]
        self._criar_janela("Relatórios", layout)

    def tela_opcoes(self) -> str:
        self.init_components()
        evento, _ = self.open()
        self.close()

        return "Voltar" if evento == sg.WIN_CLOSED else evento
