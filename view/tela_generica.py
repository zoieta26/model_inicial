import FreeSimpleGUI as sg

class TelaGenerica:
    def __init__(self):
        self.__window = None

    def _criar_janela(self, titulo: str, layout: list):
        self.__window = sg.Window(titulo, layout)

    def open(self):
        return self.__window.read()

    def close(self):
        self.__window.close()

    def mostrar_mensagem(self, msg: str):
        sg.popup(msg, title="Aviso")

    def mostrar_erro(self, msg: str):
        sg.popup_error(msg, title="Erro")

    def confirmar(self, mensagem: str) -> bool:
        return sg.popup_yes_no(mensagem, title="Confirmação") == "Yes"

    def mostrar_lista(self, titulo: str, linhas: list):
        if not linhas:
            self.mostrar_mensagem("Nenhum registro encontrado.")
            return
        sg.popup_scrolled("\n\n".join(linhas), title=titulo, size=(90, 20))

    def selecionar_da_lista(self, titulo: str, opcoes_exibicao: list, itens: list):
        layout = [
            [sg.Text(titulo, font=("Helvetica", 14))],
            [sg.Listbox(values=opcoes_exibicao, size=(70, 12), key="selecao")],
            [sg.Button("Selecionar"), sg.Button("Cancelar")]
        ]
        self._criar_janela(titulo, layout)
        evento, valores = self.open()
        self.close()

        if evento != "Selecionar" or not valores["selecao"]:
            return None

        indice = opcoes_exibicao.index(valores["selecao"][0])
        return itens[indice]
