from dao.dao import DAO

class TipoAtendimentoDAO(DAO):
    def __init__(self):
        super().__init__("tipos_atendimento.pkl")
        self.__tipos = self._carregar()

    def incluir(self, tipo):
        self.__tipos.append(tipo)
        self._salvar(self.__tipos)

    def alterar(self, tipo):
        self._salvar(self.__tipos)

    def excluir(self, tipo):
        self.__tipos.remove(tipo)
        self._salvar(self.__tipos)

    def listar(self) -> list:
        return self.__tipos
