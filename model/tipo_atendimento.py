class TipoAtendimento:
    def __init__(self, codigo: int, descricao: str):
        self.__codigo = codigo
        self.__descricao = descricao

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        self.__descricao = descricao
