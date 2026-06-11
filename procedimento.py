from model.profissional import Profissional

class Procedimento:
    def __init__(self, codigo: int, descricao: str, custo: float, responsavel: Profissional):
        self.__codigo = codigo
        self.__descricao = descricao
        self.__custo = custo
        self.__responsavel = responsavel

    @property
    def custo(self) -> float: 
        return self.__custo
    
    @property
    def descricao(self) -> str: 
        return self.__descricao