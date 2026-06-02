from datetime import time
from model.profissional import Profissional 

class Clinica: 
    def __init__(self, nome: str, cidade: str, descricao: str, hora_abertura: time, hora_fechamento: time):
        self.__nome = nome
        self.__cidade = cidade
        self.__descricao = descricao
        self.__hora_abertura = hora_abertura
        self.__hora_fechamento = hora_fechamento
        self.__profissionais = []

    @property
    def nome(self) -> str: 
        return self.__nome
    
    @property
    def cidade(self) -> str: 
        return self.__cidade
    
    @property
    def descricao(self) -> str: 
        return self.__descricao
    
    @property
    def hora_abertura(self) -> time: 
        return self.__hora_abertura
    
    @property
    def hora_fechamento(self) -> time: 
        return self.__hora_fechamento
    
    def adicionar_profissional(self, p: Profissional):
        self.__profissionais.append(p)