from model.tipo_atendimento import TipoAtendimento
from view.tela_tipo_atendimento import TelaTipoAtendimento
from dao.tipo_atendimento_dao import TipoAtendimentoDAO

class ControladorTiposAtendimento:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaTipoAtendimento()
        self.__dao = TipoAtendimentoDAO()
        self.__tipos = self.__dao.listar()

    def get_tipos(self):
        return self.__tipos

    def abrir_tela(self):
        opcoes = {
            "Cadastrar Tipo de Atendimento": self.incluir_tipo,
            "Listar Tipos de Atendimento": self.listar_tipos,
            "Editar Tipo de Atendimento": self.editar_tipo,
            "Excluir Tipo de Atendimento": self.excluir_tipo,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == "Voltar": break
            else: opcoes[opcao]()

    def incluir_tipo(self):
        descricao = self.__tela.pegar_descricao()
        if descricao is None: return

        novo_codigo = 1
        if len(self.__tipos) > 0:
            maior_codigo = max([t.codigo for t in self.__tipos])
            novo_codigo = maior_codigo + 1

        tipo = TipoAtendimento(novo_codigo, descricao)
        self.__dao.incluir(tipo)
        self.__tela.mostrar_mensagem(f"Tipo de atendimento cadastrado com sucesso! O código gerado foi: {novo_codigo}")

    def _linha_tipo(self, t: TipoAtendimento) -> str:
        return f"Cód: {t.codigo} | Descrição: {t.descricao}"

    def listar_tipos(self):
        self.__tela.mostrar_lista("Tipos de Atendimento Cadastrados", [self._linha_tipo(t) for t in self.__tipos])

    def _selecionar_tipo(self):
        if not self.__tipos:
            self.__tela.mostrar_mensagem("Nenhum tipo de atendimento cadastrado.")
            return None
        return self.__tela.selecionar_da_lista(
            "Selecione o Tipo de Atendimento", [self._linha_tipo(t) for t in self.__tipos], self.__tipos
        )

    def editar_tipo(self):
        t = self._selecionar_tipo()
        if not t: return

        nova_descricao = self.__tela.pegar_descricao(t.descricao)
        if nova_descricao is None: return

        t.descricao = nova_descricao
        self.__dao.alterar(t)
        self.__tela.mostrar_mensagem("Tipo de atendimento atualizado com sucesso!")

    def excluir_tipo(self):
        t = self._selecionar_tipo()
        if not t: return

        atendimentos_ativos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        for a in atendimentos_ativos:
            if a.tipo_atendimento.codigo == t.codigo:
                self.__tela.mostrar_erro("Este tipo de atendimento está sendo usado em atendimentos agendados! Remova os atendimentos antes de o excluir.")
                return

        self.__dao.excluir(t)
        self.__tela.mostrar_mensagem("Tipo de atendimento excluído com sucesso!")
