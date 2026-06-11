from datetime import date
from model.pessoa import Pessoa

class Profissional(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date, especialidade: str, registro_profissional: str):
        super().__init__(nome, celular, cpf, data_nascimento)
        self.__especialidade = especialidade 
        self.__registro_profissional = registro_profissional 

    @property
    def especialidade(self) -> str: 
        return self.__especialidade 
    
    @property
    def registro_profissional(self) -> str: 
        return self.__registro_profissional