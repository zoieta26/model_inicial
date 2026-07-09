from model.profissional import Profissional

class Procedimento:
    def __init__(self, codigo: int, descricao: str, custo: float, responsavel: Profissional):
        self.__codigo = codigo
        self.__descricao = descricao
        self.__custo = custo
        self.__responsavel = responsavel

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float):
        self.__custo = custo

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao

    @property
    def responsavel(self) -> Profissional:
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, responsavel: Profissional):
        self.__responsavel = responsavel