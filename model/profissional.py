from datetime import date
from model.pessoa import Pessoa
from model.clinica import Clinica

class Profissional(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date, especialidade: str, registro_profissional: str, clinica: Clinica):
        super().__init__(nome, celular, cpf, data_nascimento)
        self.__especialidade = especialidade
        self.__registro_profissional = registro_profissional
        self.__clinica = clinica

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @property
    def registro_profissional(self) -> str:
        return self.__registro_profissional

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Clinica):
        self.__clinica = clinica
