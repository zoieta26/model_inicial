from abc import ABC
from datetime import date

class Pessoa(ABC):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date):
        self.__nome = nome
        self.__celular = celular
        self.__cpf = cpf
        self.__data_nascimento = data_nascimento 

    @property
    def nome(self) -> str: 
        return self.__nome
    @nome.setter
    def nome(self, nome: str): 
        self.__nome = nome
    
    @property
    def celular(self) -> str: 
        return self.__celular
    
    @celular.setter
    def celular(self, celular: str): 
        self.__celular = celular
    
    @property
    def cpf(self) -> str: 
        return self.__cpf
    
    @property
    def data_nascimento(self) -> date: 
        return self.__data_nascimento