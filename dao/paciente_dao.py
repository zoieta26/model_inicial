from dao.dao import DAO

class PacienteDAO(DAO):
    def __init__(self):
        super().__init__("pacientes.pkl")
        self.__pacientes = self._carregar()

    def incluir(self, paciente):
        self.__pacientes.append(paciente)
        self._salvar(self.__pacientes)

    def alterar(self, paciente):
        self._salvar(self.__pacientes)

    def excluir(self, paciente):
        self.__pacientes.remove(paciente)
        self._salvar(self.__pacientes)

    def listar(self) -> list:
        return self.__pacientes
