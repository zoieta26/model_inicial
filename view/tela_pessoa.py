from datetime import datetime
import FreeSimpleGUI as sg
from view.tela_generica import TelaGenerica

class TelaPessoa(TelaGenerica):
    def __init__(self):
        super().__init__()
        self.init_components()

    def init_components(self):
        layout = [
            [sg.Text("MÓDULO PESSOAS", font=("Helvetica", 18))],
            [sg.Text("Pacientes", font=("Helvetica", 12, "bold"))],
            [sg.Button("Cadastrar Paciente", size=(22, 1)), sg.Button("Listar Pacientes", size=(22, 1))],
            [sg.Button("Editar Paciente", size=(22, 1)), sg.Button("Excluir Paciente", size=(22, 1))],
            [sg.Text("Profissionais", font=("Helvetica", 12, "bold"))],
            [sg.Button("Cadastrar Profissional", size=(22, 1)), sg.Button("Listar Profissionais", size=(22, 1))],
            [sg.Button("Editar Profissional", size=(22, 1)), sg.Button("Excluir Profissional", size=(22, 1))],
            [sg.Button("Voltar", size=(22, 1))]
        ]
        self._criar_janela("Pessoas", layout)

    def tela_opcoes(self) -> str:
        self.init_components()
        evento, _ = self.open()
        self.close()

        return "Voltar" if evento == sg.WIN_CLOSED else evento

    def init_formulario_base(self, dados_atuais: dict = None):
        d = dados_atuais or {}
        layout = [
            [sg.Text("Nome:", size=(28, 1)), sg.InputText(d.get("nome", ""), key="nome")],
            [sg.Text("Celular:", size=(28, 1)), sg.InputText(d.get("celular", ""), key="celular")],
            [sg.Text("CPF:", size=(28, 1)), sg.InputText(d.get("cpf", ""), key="cpf")],
            [sg.Text("Data de Nascimento (DD/MM/AAAA):", size=(28, 1)), sg.InputText(d.get("data_nascimento", ""), key="data_nascimento")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Cadastro", layout)

    def pegar_dados_base(self) -> dict:
        d = None
        while True:
            self.init_formulario_base(d)
            evento, valores = self.open()
            self.close()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                return None

            try:
                data_nasc = datetime.strptime(valores["data_nascimento"], "%d/%m/%Y").date()
            except ValueError:
                self.mostrar_erro("Data de nascimento em formato inválido. Use DD/MM/AAAA.")
                d = valores
                continue

            return {"nome": valores["nome"], "celular": valores["celular"], "cpf": valores["cpf"], "data_nascimento": data_nasc}

    def init_formulario_edicao_pessoa(self, nome_atual: str, celular_atual: str):
        layout = [
            [sg.Text("Nome:", size=(12, 1)), sg.InputText(nome_atual, key="nome")],
            [sg.Text("Celular:", size=(12, 1)), sg.InputText(celular_atual, key="celular")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Editar Dados", layout)

    def pegar_dados_edicao_pessoa(self, nome_atual: str, celular_atual: str) -> dict:
        self.init_formulario_edicao_pessoa(nome_atual, celular_atual)
        evento, valores = self.open()
        self.close()

        if evento in (sg.WIN_CLOSED, "Cancelar"):
            return None
        return {"nome": valores["nome"], "celular": valores["celular"]}

    def init_formulario_profissional(self):
        layout = [
            [sg.Text("Especialidade:", size=(18, 1)), sg.InputText(key="especialidade")],
            [sg.Text("Registro (CRM/COREN):", size=(18, 1)), sg.InputText(key="registro")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Dados Profissionais", layout)

    def pegar_dados_profissional(self) -> dict:
        self.init_formulario_profissional()
        evento, valores = self.open()
        self.close()

        if evento in (sg.WIN_CLOSED, "Cancelar"):
            return None
        return {"especialidade": valores["especialidade"], "registro": valores["registro"]}
