from datetime import datetime
import FreeSimpleGUI as sg
from view.tela_generica import TelaGenerica

class TelaAtendimento(TelaGenerica):
    def __init__(self):
        super().__init__()
        self.init_components()

    def init_components(self):
        layout = [
            [sg.Text("MÓDULO ATENDIMENTOS", font=("Helvetica", 18))],
            [sg.Text("Atendimento", font=("Helvetica", 12, "bold"))],
            [sg.Button("Agendar Atendimento", size=(24, 1)), sg.Button("Listar Atendimentos", size=(24, 1))],
            [sg.Button("Editar Atendimento", size=(24, 1)), sg.Button("Cancelar/Excluir Atendimento", size=(24, 1))],
            [sg.Text("Procedimento", font=("Helvetica", 12, "bold"))],
            [sg.Button("Adicionar Procedimento", size=(24, 1)), sg.Button("Editar Procedimento", size=(24, 1))],
            [sg.Button("Excluir Procedimento", size=(24, 1))],
            [sg.Text("Pagamento", font=("Helvetica", 12, "bold"))],
            [sg.Button("Registrar Pagamento", size=(24, 1)), sg.Button("Editar Pagamento", size=(24, 1))],
            [sg.Button("Excluir Pagamento", size=(24, 1))],
            [sg.Button("Voltar", size=(24, 1))]
        ]
        self._criar_janela("Atendimentos", layout)

    def tela_opcoes(self) -> str:
        self.init_components()
        evento, _ = self.open()
        self.close()

        return "Voltar" if evento == sg.WIN_CLOSED else evento


    def init_formulario_atendimento(self, dados_atuais: dict = None):
        d = dados_atuais or {}
        layout = [
            [sg.Text("Código do Atendimento (número):", size=(28, 1)), sg.InputText(d.get("codigo", ""), key="codigo")],
            [sg.Text("Data do Atendimento (DD/MM/AAAA):", size=(28, 1)), sg.InputText(d.get("data", ""), key="data")],
            [sg.Text("Hora da Consulta (HH:MM):", size=(28, 1)), sg.InputText(d.get("hora_inicio", ""), key="hora_inicio")],
            [sg.Text("Valor Base (R$):", size=(28, 1)), sg.InputText(d.get("valor_base", ""), key="valor_base")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Dados do Atendimento", layout)

    def pegar_dados_atendimento(self) -> dict:
        d = None
        while True:
            self.init_formulario_atendimento(d)
            evento, valores = self.open()
            self.close()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                return None

            try:
                codigo = int(valores["codigo"])
                data_atendimento = datetime.strptime(valores["data"], "%d/%m/%Y").date()
                hora_inicio = datetime.strptime(valores["hora_inicio"], "%H:%M").time()
                valor_base = float(valores["valor_base"].replace(",", "."))
            except ValueError:
                self.mostrar_erro("Formato inválido. Verifique código, data, hora e valor.")
                d = valores
                continue

            return {"codigo": codigo, "data": data_atendimento, "hora_inicio": hora_inicio, "valor_base": valor_base}

    def init_formulario_edicao_atendimento(self, dados_atuais: dict = None):
        d = dados_atuais or {}
        layout = [
            [sg.Text("Nova Data do Atendimento (DD/MM/AAAA):", size=(28, 1)), sg.InputText(d.get("data", ""), key="data")],
            [sg.Text("Nova Hora da Consulta (HH:MM):", size=(28, 1)), sg.InputText(d.get("hora_inicio", ""), key="hora_inicio")],
            [sg.Text("Novo Valor Base (R$):", size=(28, 1)), sg.InputText(d.get("valor_base", ""), key="valor_base")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Editar Atendimento", layout)

    def pegar_dados_edicao_atendimento(self, data_atual: str = "", hora_atual: str = "", valor_atual: str = "") -> dict:
        d = {"data": data_atual, "hora_inicio": hora_atual, "valor_base": valor_atual}
        while True:
            self.init_formulario_edicao_atendimento(d)
            evento, valores = self.open()
            self.close()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                return None

            try:
                data_atendimento = datetime.strptime(valores["data"], "%d/%m/%Y").date()
                hora_inicio = datetime.strptime(valores["hora_inicio"], "%H:%M").time()
                valor_base = float(valores["valor_base"].replace(",", "."))
            except ValueError:
                self.mostrar_erro("Formato inválido. Verifique data, hora e valor.")
                d = valores
                continue

            return {"data": data_atendimento, "hora_inicio": hora_inicio, "valor_base": valor_base}


    def init_formulario_procedimento(self, dados_atuais: dict = None):
        d = dados_atuais or {}
        layout = [
            [sg.Text("Código do Procedimento (número):", size=(30, 1)), sg.InputText(d.get("codigo", ""), key="codigo")],
            [sg.Text("Descrição (ex: Raio-X, Análises Clínicas):", size=(30, 1)), sg.InputText(d.get("descricao", ""), key="descricao")],
            [sg.Text("Custo Adicional (R$):", size=(30, 1)), sg.InputText(d.get("custo", ""), key="custo")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Adicionar Procedimento", layout)

    def pegar_dados_procedimento(self) -> dict:
        d = None
        while True:
            self.init_formulario_procedimento(d)
            evento, valores = self.open()
            self.close()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                return None

            try:
                codigo = int(valores["codigo"])
                custo = float(valores["custo"].replace(",", "."))
            except ValueError:
                self.mostrar_erro("Verifique se o código é um número inteiro e o custo é um valor numérico válido.")
                d = valores
                continue

            return {"codigo": codigo, "descricao": valores["descricao"], "custo": custo}

    def init_formulario_edicao_procedimento(self, dados_atuais: dict = None):
        d = dados_atuais or {}
        layout = [
            [sg.Text("Nova Descrição:", size=(15, 1)), sg.InputText(d.get("descricao", ""), key="descricao")],
            [sg.Text("Novo Custo (R$):", size=(15, 1)), sg.InputText(d.get("custo", ""), key="custo")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Editar Procedimento", layout)

    def pegar_dados_edicao_procedimento(self, descricao_atual: str = "", custo_atual: float = None) -> dict:
        d = {"descricao": descricao_atual, "custo": f"{custo_atual:.2f}" if custo_atual is not None else ""}
        while True:
            self.init_formulario_edicao_procedimento(d)
            evento, valores = self.open()
            self.close()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                return None

            try:
                custo = float(valores["custo"].replace(",", "."))
            except ValueError:
                self.mostrar_erro("Digite um valor numérico válido.")
                d = valores
                continue

            return {"descricao": valores["descricao"], "custo": custo}


    def init_formulario_pagamento(self, valor_total: float, valor_pago: float, valor_restante: float, dados_atuais: dict = None):
        d = dados_atuais or {}
        layout = [
            [sg.Text(f"Valor Total do Atendimento (Consulta + Procedimentos): R$ {valor_total:.2f}")],
            [sg.Text(f"Já Pago: R$ {valor_pago:.2f}")],
            [sg.Text(f"Restante: R$ {valor_restante:.2f}")],
            [sg.Text("Código do Pagamento (número):", size=(28, 1)), sg.InputText(d.get("codigo", ""), key="codigo")],
            [sg.Text("Modalidade:")],
            [sg.Radio("Dinheiro", "MODALIDADE", key="dinheiro", default=True),
             sg.Radio("PIX", "MODALIDADE", key="pix"),
             sg.Radio("Cartão de Crédito", "MODALIDADE", key="cartao")],
            [sg.Text(f"Valor a pagar agora (máx R$ {valor_restante:.2f}):", size=(28, 1)), sg.InputText(d.get("valor", ""), key="valor")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Registrar Pagamento", layout)

    def init_formulario_pix(self):
        layout = [
            [sg.Text("CPF do pagador:"), sg.InputText(key="cpf_pagador")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Dados do PIX", layout)

    def init_formulario_cartao(self):
        layout = [
            [sg.Text("Número do Cartão:"), sg.InputText(key="numero_cartao")],
            [sg.Text("Bandeira (ex: Visa, Mastercard):"), sg.InputText(key="bandeira")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Dados do Cartão", layout)

    def pegar_dados_pagamento(self, valor_total: float, valor_pago: float, valor_restante: float) -> dict:
        d = None
        while True:
            self.init_formulario_pagamento(valor_total, valor_pago, valor_restante, d)
            evento, valores = self.open()
            self.close()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                return None

            try:
                codigo = int(valores["codigo"])
                valor = float(valores["valor"].replace(",", "."))
            except ValueError:
                self.mostrar_erro("Verifique se o código é um número inteiro e o valor é um número válido.")
                d = valores
                continue

            if valor <= 0 or valor > valor_restante:
                self.mostrar_erro(f"O valor deve ser maior que zero e no máximo R$ {valor_restante:.2f}.")
                d = valores
                continue

            tipo = 1 if valores["dinheiro"] else 2 if valores["pix"] else 3
            dados = {"codigo": codigo, "tipo": tipo, "valor": valor}

            if tipo == 2:
                self.init_formulario_pix()
                evento2, valores2 = self.open()
                self.close()
                if evento2 in (sg.WIN_CLOSED, "Cancelar"):
                    return None
                dados["cpf_pagador"] = valores2["cpf_pagador"]
            elif tipo == 3:
                self.init_formulario_cartao()
                evento2, valores2 = self.open()
                self.close()
                if evento2 in (sg.WIN_CLOSED, "Cancelar"):
                    return None
                dados["numero_cartao"] = valores2["numero_cartao"]
                dados["bandeira"] = valores2["bandeira"]

            return dados

    def init_formulario_valor_pagamento(self, valor_atual: str = ""):
        layout = [
            [sg.Text("Novo valor pago (R$):")],
            [sg.InputText(valor_atual, key="valor")],
            [sg.Button("Confirmar"), sg.Button("Cancelar")]
        ]
        self._criar_janela("Editar Pagamento", layout)

    def pegar_novo_valor_pagamento(self, valor_atual: float = None) -> float:
        d = f"{valor_atual:.2f}" if valor_atual is not None else ""
        while True:
            self.init_formulario_valor_pagamento(d)
            evento, valores = self.open()
            self.close()

            if evento in (sg.WIN_CLOSED, "Cancelar"):
                return None

            try:
                return float(valores["valor"].replace(",", "."))
            except ValueError:
                self.mostrar_erro("Digite um valor numérico válido.")
                d = valores["valor"]
