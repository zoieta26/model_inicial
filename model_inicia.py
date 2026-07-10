from abc import ABC, abstractmethod
from datetime import date, time

# --- CLASSES ABSTRATAS E HERANÇAS (PESSOAS) ---

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
    def nome(self, novo_nome: str):
        self.__nome = novo_nome

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, novo_celular: str):
        self.__celular = novo_celular

    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    def idade(self) -> int:
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))

    @abstractmethod
    def tipo(self) -> str:
        pass


class Paciente(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date):
        super().__init__(nome, celular, cpf, data_nascimento)

    def tipo(self) -> str:
        return "Paciente"


class Profissional(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str, data_nascimento: date, especialidade: str, registro_profissional: str):
        super().__init__(nome, celular, cpf, data_nascimento)
        self.__especialidade = especialidade
        self.__registro_profissional = registro_profissional

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, nova_especialidade: str):
        self.__especialidade = nova_especialidade

    @property
    def registro_profissional(self) -> str:
        return self.__registro_profissional

    def tipo(self) -> str:
        return "Profissional"


# --- CLASSES BASE DE REGISTRO ---

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
    def hora_abertura(self) -> time:
        return self.__hora_abertura
        
    @property
    def hora_fechamento(self) -> time:
        return self.__hora_fechamento

    def adicionarProfissional(self, p: Profissional):
        self.__profissionais.append(p)


class TipoAtendimento:
    def __init__(self, nome: str, descricao: str):
        self.__nome = nome
        self.__descricao = descricao


class Procedimento:
    def __init__(self, codigo: int, descricao: str, custo: float, responsavel: Profissional):
        self.__codigo = codigo
        self.__descricao = descricao
        self.__custo = custo
        self.__responsavel = responsavel 

    @property
    def custo(self) -> float:
        return self.__custo


# --- CLASSES ABSTRATAS E HERANÇAS (PAGAMENTOS) ---

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
        return "Dinheiro"

    def detalhes(self) -> str:
        return "Pagamento realizado em espécie."


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
        return f"Cartão {self.__bandeira} - Final {self.__numero_cartao[-4:]}"


# --- CLASSE CENTRAL (ATENDIMENTO) ---

class Atendimento:
    def __init__(self, codigo: int, data_atendimento: date, hora_inicio: time, hora_fim: time, clinica: Clinica, paciente: Paciente, profissional: Profissional, tipo_atendimento: TipoAtendimento, valor_base: float):
        
        # Validando Regras de Negócio exigidas
        if paciente.idade() < 18:
            raise ValueError("Somente pacientes com mais de 18 anos completos podem realizar atendimentos de forma independente.")
            
        if hora_inicio < clinica.hora_abertura or hora_fim > clinica.hora_fechamento:
            raise ValueError("Os atendimentos devem ocorrer dentro do período de funcionamento da clínica.")
            
        self.__codigo = codigo
        self.__data = data_atendimento
        self.__hora_inicio = hora_inicio
        self.__hora_fim = hora_fim
        self.__valor = valor_base
        
        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__tipo_atendimento = tipo_atendimento
        
        self.__procedimentos = []
        self.__pagamentos = []

    def adicionarProcedimento(self, p: Procedimento):
        self.__procedimentos.append(p)

    def adicionarPagamento(self, p: Pagamento):
        self.__pagamentos.append(p)

    def valorTotal(self) -> float:
        custo_procedimentos = sum(proc.custo for proc in self.__procedimentos)
        return self.__valor + custo_procedimentos

    def valorPago(self) -> float:
        return sum(pag.valor_pago for pag in self.__pagamentos)

    def valorRestante(self) -> float:
        return self.valorTotal() - self.valorPago()
