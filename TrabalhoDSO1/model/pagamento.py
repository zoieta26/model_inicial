from abc import ABC, abstractmethod
from datetime import date

class Pagamento(ABC):
    def __init__(self, codigo: int, data_pagamento: date, valor_pago: float):
        self.__codigo = codigo
        self.__data_pagamento = data_pagamento
        self.__valor_pago = valor_pago

    @property
    def valor_pago(self) -> float: 
        return self.__valor_pago
    
    @abstractmethod
    def modalidade(self) -> str: 
        pass
    
    @abstractmethod
    def detalhes(self) -> str: 
        pass

class PagamentoDinheiro(Pagamento):
    def modalidade(self) -> str: 
        return "DINHEIRO"
    def detalhes(self) -> str: 
        return f"Valor pago: R${self.valor_pago:.2f}"

class PagamentoPix(Pagamento):
    def __init__(self, codigo: int, data_pagamento: date, valor_pago: float, cpf_pagador: str):
        super().__init__(codigo, data_pagamento, valor_pago)
        self.__cpf_pagador = cpf_pagador

    def modalidade(self) -> str: 
        return "PIX"
    def detalhes(self) -> str: 
        return f"PIX - CPF: {self.__cpf_pagador}"

class PagamentoCartao(Pagamento):
    def __init__(self, codigo: int, data_pagamento: date, valor_pago: float, numero_cartao: str, bandeira: str):
        super().__init__(codigo, data_pagamento, valor_pago)
        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    def modalidade(self) -> str: 
        return "Cartão de Crédito"
    
    def detalhes(self) -> str: 
        return f"Cartão {self.__bandeira} - Final: {self.__numero_cartao[-4:]}"