from model.clinica import Clinica
from view.tela_clinica import TelaClinica

class ControladorClinicas:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaClinica()
        self.__clinicas = []

    def abrir_tela(self):
        opcoes = {1: self.incluir_clinica, 2: self.listar_clinicas, 3: self.excluir_clinica}
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0: break 
            else: opcoes[opcao]()

    def incluir_clinica(self):
        dados = self.__tela.pegar_dados_clinica()
        clinica = Clinica(
            dados["nome"], dados["cidade"], dados["descricao"], 
            dados["hora_abertura"], dados["hora_fechamento"]
        )
        self.__clinicas.append(clinica)
        self.__tela.mostrar_mensagem("Clínica cadastrada com sucesso!")

    def listar_clinicas(self):
        if not self.__clinicas:
            self.__tela.mostrar_mensagem("Nenhuma clínica cadastrada.")
            return
        for c in self.__clinicas:
            abertura = c.hora_abertura.strftime("%H:%M")
            fechamento = c.hora_fechamento.strftime("%H:%M")
            self.__tela.mostrar_mensagem(f"Clínica: {c.nome} | Cidade: {c.cidade} | Funcionamento: {abertura} às {fechamento}")

    def excluir_clinica(self):
        self.listar_clinicas()
        if not self.__clinicas: return
        nome = input("\nDigite o NOME EXATO da clínica que deseja excluir: ")
        for c in self.__clinicas:
            if c.nome.lower() == nome.lower():
                self.__clinicas.remove(c)
                self.__tela.mostrar_mensagem("Clínica excluída com sucesso!")
                return
        self.__tela.mostrar_mensagem("Clínica não encontrada.")

    def get_clinicas(self):
        return self.__clinicas