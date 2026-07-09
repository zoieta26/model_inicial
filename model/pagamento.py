from abc import ABC, abstractmethod
from datetime import date

class Pagamento(ABC):
    def __init__(self, codigo: int, data_pagamento: date, valor_pago: float, atendimento, paciente):
        # REGRA DE NEGÓCIO: pagamentos devem ser realizados até a data do atendimento
        if data_pagamento > atendimento.data_atendimento:
            raise ValueError(
                f"Pagamento ({data_pagamento.strftime('%d/%m/%Y')}) deve ser realizado até a data do atendimento ({atendimento.data_atendimento.strftime('%d/%m/%Y')})."
            )

        self.__codigo = codigo
        self.__data_pagamento = data_pagamento
        self.__valor_pago = valor_pago
        self.__atendimento = atendimento
        self.__paciente = paciente

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def data_pagamento(self) -> date:
        return self.__data_pagamento

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, novo_valor: float):
        maximo_permitido = self.__atendimento.valorRestante() + self.__valor_pago
        if novo_valor <= 0 or novo_valor > maximo_permitido:
            raise ValueError(f"O valor deve ser maior que zero e no máximo R$ {maximo_permitido:.2f}.")
        self.__valor_pago = novo_valor

    @property
    def atendimento(self):
        return self.__atendimento

    @property
    def paciente(self):
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente):
        self.__paciente = paciente

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
    def __init__(self, codigo: int, data_pagamento: date, valor_pago: float, atendimento, paciente, cpf_pagador: str):
        super().__init__(codigo, data_pagamento, valor_pago, atendimento, paciente)
        self.__cpf_pagador = cpf_pagador

    def modalidade(self) -> str:
        return "PIX"
    def detalhes(self) -> str:
        return f"PIX - CPF: {self.__cpf_pagador}"

class PagamentoCartao(Pagamento):
    def __init__(self, codigo: int, data_pagamento: date, valor_pago: float, atendimento, paciente, numero_cartao: str, bandeira: str):
        super().__init__(codigo, data_pagamento, valor_pago, atendimento, paciente)
        self.__numero_cartao = numero_cartao
        self.__bandeira = bandeira

    def modalidade(self) -> str:
        return "Cartão de Crédito"

    def detalhes(self) -> str:
        return f"Cartão {self.__bandeira} - Final: {self.__numero_cartao[-4:]}"
