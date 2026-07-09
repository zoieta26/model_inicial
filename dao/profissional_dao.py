from dao.dao import DAO

class ProfissionalDAO(DAO):
    def __init__(self):
        super().__init__("profissionais.pkl")
        self.__profissionais = self._carregar()

    def incluir(self, profissional):
        self.__profissionais.append(profissional)
        self._salvar(self.__profissionais)

    def alterar(self, profissional):
        self._salvar(self.__profissionais)

    def excluir(self, profissional):
        self.__profissionais.remove(profissional)
        self._salvar(self.__profissionais)

    def listar(self) -> list:
        return self.__profissionais
