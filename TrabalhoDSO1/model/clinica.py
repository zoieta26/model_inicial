from datetime import time
from model.profissional import Profissional 

class Clinica: 
    def __init__(self, codigo: int, nome: str, cidade: str, descricao: str, hora_abertura: time, hora_fechamento: time):
        self.__codigo = codigo
        self.__nome = nome
        self.__cidade = cidade
        self.__descricao = descricao
        self.__hora_abertura = hora_abertura
        self.__hora_fechamento = hora_fechamento
        self.__profissionais = []

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def nome(self) -> str: 
        return self.__nome
    
    @nome.setter
    def nome(self, nome: str): 
        self.__nome = nome

    @property
    def cidade(self) -> str: 
        return self.__cidade
    
    @cidade.setter
    def cidade(self, cidade: str): 
        self.__cidade = cidade

    @property
    def descricao(self) -> str: 
        return self.__descricao
    
    @descricao.setter
    def descricao(self, descricao: str): 
        self.__descricao = descricao

    @property
    def hora_abertura(self) -> time: 
        return self.__hora_abertura
    
    @hora_abertura.setter
    def hora_abertura(self, hora: time): 
        self.__hora_abertura = hora

    @property
    def hora_fechamento(self) -> time: 
        return self.__hora_fechamento
    
    @hora_fechamento.setter
    def hora_fechamento(self, hora: time): 
        self.__hora_fechamento = hora
    
    def adicionar_profissional(self, p: Profissional):
        self.__profissionais.append(p)