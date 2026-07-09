from dao.dao import DAO

class ClinicaDAO(DAO):
    def __init__(self):
        super().__init__("clinicas.pkl")
        self.__clinicas = self._carregar()

    def incluir(self, clinica):
        self.__clinicas.append(clinica)
        self._salvar(self.__clinicas)

    def alterar(self, clinica):
        self._salvar(self.__clinicas)

    def excluir(self, clinica):
        self.__clinicas.remove(clinica)
        self._salvar(self.__clinicas)

    def listar(self) -> list:
        return self.__clinicas
