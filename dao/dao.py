import os
import pickle
from abc import ABC, abstractmethod

DIRETORIO_DADOS = "dados"

class DAO(ABC):
    def __init__(self, nome_arquivo: str):
        os.makedirs(DIRETORIO_DADOS, exist_ok=True)
        self.__caminho = os.path.join(DIRETORIO_DADOS, nome_arquivo)

    def _salvar(self, lista: list):
        with open(self.__caminho, 'wb') as arquivo:
            pickle.dump(lista, arquivo)

    def _carregar(self) -> list:
        try:
            with open(self.__caminho, 'rb') as arquivo:
                return pickle.load(arquivo)
        except (FileNotFoundError, EOFError):
            return []

    @abstractmethod
    def incluir(self, objeto):
        pass

    @abstractmethod
    def alterar(self, objeto):
        pass

    @abstractmethod
    def excluir(self, objeto):
        pass

    @abstractmethod
    def listar(self) -> list:
        pass
