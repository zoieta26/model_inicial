import FreeSimpleGUI as sg
from view.tela_generica import TelaGenerica

class TelaTipoAtendimento(TelaGenerica):
    def __init__(self):
        super().__init__()
        self.init_components()

    def init_components(self):
        layout = [
            [sg.Text("TIPOS DE ATENDIMENTO", font=("Helvetica", 18))],
            [sg.Button("Cadastrar Tipo de Atendimento", size=(28, 1))],
            [sg.Button("Listar Tipos de Atendimento", size=(28, 1))],
            [sg.Button("Editar Tipo de Atendimento", size=(28, 1))],
            [sg.Button("Excluir Tipo de Atendimento", size=(28, 1))],
            [sg.Button("Voltar", size=(28, 1))]
        ]
        self._criar_janela("Tipos de Atendimento", layout)

    def tela_opcoes(self) -> str:
        self.init_components()
        evento, _ = self.open()
        self.close()

        return "Voltar" if evento == sg.WIN_CLOSED else evento

    def init_formulario_descricao(self, descricao_atual: str = ""):
        layout = [
            [sg.Text("Descrição (ex: Consulta, Exame, Retorno):")],
            [sg.InputText(descricao_atual, key="descricao")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Tipo de Atendimento", layout)

    def pegar_descricao(self, descricao_atual: str = "") -> str:
        self.init_formulario_descricao(descricao_atual)
        evento, valores = self.open()
        self.close()

        if evento in (sg.WIN_CLOSED, "Cancelar"):
            return None
        return valores["descricao"]
