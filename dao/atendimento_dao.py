from dao.dao import DAO

class AtendimentoDAO(DAO):
    def __init__(self):
        super().__init__("atendimentos.pkl")
        self.__atendimentos = self._carregar()

    def incluir(self, atendimento):
        self.__atendimentos.append(atendimento)
        self._salvar(self.__atendimentos)

    def alterar(self, atendimento):
        self._salvar(self.__atendimentos)

    def excluir(self, atendimento):
        self.__atendimentos.remove(atendimento)
        self._salvar(self.__atendimentos)

    def listar(self) -> list:
        return self.__atendimentos
