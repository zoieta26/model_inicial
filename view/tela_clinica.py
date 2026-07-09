from datetime import datetime
import FreeSimpleGUI as sg
from view.tela_generica import TelaGenerica

class TelaClinica(TelaGenerica):
    def __init__(self):
        super().__init__()
        self.init_components()

    def init_components(self):
        layout = [
            [sg.Text("MÓDULO CLÍNICAS", font=("Helvetica", 18))],
            [sg.Button("Cadastrar Clínica", size=(20, 1))],
            [sg.Button("Listar Clínicas", size=(20, 1))],
            [sg.Button("Editar Clínica", size=(20, 1))],
            [sg.Button("Excluir Clínica", size=(20, 1))],
            [sg.Button("Voltar", size=(20, 1))]
        ]
        self._criar_janela("Clínicas", layout)

    def tela_opcoes(self) -> str:
        self.init_components()
        evento, _ = self.open()
        self.close()

        return "Voltar" if evento == sg.WIN_CLOSED else evento

    def init_formulario_clinica(self, dados_atuais: dict = None):
        d = dados_atuais or {}
        layout = [
            [sg.Text("Nome da Clínica:", size=(22, 1)), sg.InputText(d.get("nome", ""), key="nome")],
            [sg.Text("Cidade:", size=(22, 1)), sg.InputText(d.get("cidade", ""), key="cidade")],
            [sg.Text("Descrição:", size=(22, 1)), sg.InputText(d.get("descricao", ""), key="descricao")],
            [sg.Text("Hora de Abertura (HH:MM):", size=(22, 1)), sg.InputText(d.get("hora_abertura", ""), key="hora_abertura")],
            [sg.Text("Hora de Fechamento (HH:MM):", size=(22, 1)), sg.InputText(d.get("hora_fechamento", ""), key="hora_fechamento")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Dados da Clínica", layout)

    def pegar_dados_clinica(self, dados_atuais: dict = None) -> dict:
        hora_limite = datetime.strptime("18:30", "%H:%M").time()
        d = dados_atuais

        while True:
            self.init_formulario_clinica(d)
            evento, valores = self.open()
            self.close()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                return None

            try:
                hora_abertura = datetime.strptime(valores["hora_abertura"], "%H:%M").time()
                hora_fechamento = datetime.strptime(valores["hora_fechamento"], "%H:%M").time()
            except ValueError:
                self.mostrar_erro("Formato de hora inválido. Use HH:MM (ex: 08:00, 18:30).")
                d = valores
                continue

            if hora_fechamento > hora_limite:
                self.mostrar_erro("As clínicas operam no máximo até as 18:30. Digite um horário válido.")
                d = valores
                continue

            return {
                "nome": valores["nome"],
                "cidade": valores["cidade"],
                "descricao": valores["descricao"],
                "hora_abertura": hora_abertura,
                "hora_fechamento": hora_fechamento
            }
