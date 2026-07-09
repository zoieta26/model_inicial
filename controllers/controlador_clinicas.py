from model.clinica import Clinica
from view.tela_clinica import TelaClinica
from dao.clinica_dao import ClinicaDAO

class ControladorClinicas:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaClinica()
        self.__dao = ClinicaDAO()
        self.__clinicas = self.__dao.listar()

    def abrir_tela(self):
        opcoes = {
            "Cadastrar Clínica": self.incluir_clinica,
            "Listar Clínicas": self.listar_clinicas,
            "Editar Clínica": self.editar_clinica,
            "Excluir Clínica": self.excluir_clinica,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == "Voltar": break
            else: opcoes[opcao]()

    def incluir_clinica(self):
        dados = self.__tela.pegar_dados_clinica()
        if dados is None: return

        novo_codigo = 1
        if len(self.__clinicas) > 0:
            maior_codigo = max([c.codigo for c in self.__clinicas])
            novo_codigo = maior_codigo + 1

        clinica = Clinica(
            novo_codigo,
            dados["nome"],
            dados["cidade"],
            dados["descricao"],
            dados["hora_abertura"],
            dados["hora_fechamento"]
        )
        self.__dao.incluir(clinica)
        self.__tela.mostrar_mensagem(f"Clínica cadastrada com sucesso! O código gerado foi: {novo_codigo}")

    def _linha_clinica(self, c: Clinica) -> str:
        abertura = c.hora_abertura.strftime("%H:%M")
        fechamento = c.hora_fechamento.strftime("%H:%M")
        return f"Cód: {c.codigo} | Clínica: {c.nome} | Cidade: {c.cidade} | Funcionamento: {abertura} às {fechamento}"

    def listar_clinicas(self):
        self.__tela.mostrar_lista("Clínicas Cadastradas", [self._linha_clinica(c) for c in self.__clinicas])

    def _selecionar_clinica(self):
        if not self.__clinicas:
            self.__tela.mostrar_mensagem("Nenhuma clínica cadastrada.")
            return None
        return self.__tela.selecionar_da_lista(
            "Selecione a Clínica", [self._linha_clinica(c) for c in self.__clinicas], self.__clinicas
        )

    def editar_clinica(self):
        c = self._selecionar_clinica()
        if not c: return

        dados_atuais = {
            "nome": c.nome,
            "cidade": c.cidade,
            "descricao": c.descricao,
            "hora_abertura": c.hora_abertura.strftime("%H:%M"),
            "hora_fechamento": c.hora_fechamento.strftime("%H:%M"),
        }
        novos_dados = self.__tela.pegar_dados_clinica(dados_atuais)
        if novos_dados is None: return

        c.nome = novos_dados["nome"]
        c.cidade = novos_dados["cidade"]
        c.descricao = novos_dados["descricao"]
        c.hora_abertura = novos_dados["hora_abertura"]
        c.hora_fechamento = novos_dados["hora_fechamento"]

        self.__dao.alterar(c)
        self.__tela.mostrar_mensagem("Dados da clínica atualizados com sucesso!")

    def excluir_clinica(self):
        c = self._selecionar_clinica()
        if not c: return

        atendimentos_ativos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        for a in atendimentos_ativos:
            if a.clinica.codigo == c.codigo:
                self.__tela.mostrar_erro("Esta clínica tem consultas agendadas! Remova os atendimentos antes de a excluir.")
                return

        profissionais_ativos = self.__ctrl_principal.ctrl_pessoas.profissionais
        for p in profissionais_ativos:
            if p.clinica.codigo == c.codigo:
                self.__tela.mostrar_erro("Esta clínica possui profissionais vinculados! Remova os profissionais antes de a excluir.")
                return

        self.__dao.excluir(c)
        self.__tela.mostrar_mensagem("Clínica excluída com sucesso!")

    def get_clinicas(self):
        return self.__clinicas
