from datetime import date, time, datetime, timedelta
from model.clinica import Clinica
from model.paciente import Paciente
from model.profissional import Profissional
from model.procedimento import Procedimento
from model.pagamento import Pagamento
from model.tipo_atendimento import TipoAtendimento

class Atendimento:
    def __init__(self, codigo: int, data_atendimento: date, hora_marcada: time, clinica: Clinica, paciente: Paciente, profissional: Profissional, tipo_atendimento: TipoAtendimento, valor_base: float):

        hoje = date.today()
        inicio_dt = datetime.combine(hoje, hora_marcada)
        fim_dt = inicio_dt + timedelta(minutes=30)
        hora_fim_calculada = fim_dt.time()

        if paciente.idade() < 18:
            raise ValueError("Pacientes menores de 18 anos não podem ser agendados sozinhos.")

        if hora_marcada < clinica.hora_abertura or hora_fim_calculada > clinica.hora_fechamento:
            raise ValueError(f"A consulta ({hora_marcada.strftime('%H:%M')} às {hora_fim_calculada.strftime('%H:%M')}) ultrapassa o horário de funcionamento da clínica.")

        self.__codigo = codigo
        self.__data_atendimento = data_atendimento
        self.__hora_inicio = hora_marcada
        self.__hora_fim = hora_fim_calculada
        self.__valor = valor_base

        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional  # Salvando o médico responsável!
        self.__tipo_atendimento = tipo_atendimento
        self.__procedimentos = []
        self.__pagamentos = []

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @property
    def data_atendimento(self) -> date:
        return self.__data_atendimento

    @property
    def hora_inicio(self) -> time:
        return self.__hora_inicio

    @property
    def hora_fim(self) -> time:
        return self.__hora_fim

    @property
    def valor_base(self) -> float:
        return self.__valor

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @property
    def profissional(self) -> Profissional:
        return self.__profissional

    @property
    def tipo_atendimento(self) -> TipoAtendimento:
        return self.__tipo_atendimento

    @property
    def procedimentos(self) -> list:
        return list(self.__procedimentos)

    @property
    def pagamentos(self) -> list:
        return list(self.__pagamentos)

    def adicionarProcedimento(self, p: Procedimento):
        self.__procedimentos.append(p)

    def removerProcedimento(self, p: Procedimento):
        self.__procedimentos.remove(p)

    def adicionarPagamento(self, p: Pagamento):
        self.__pagamentos.append(p)

    def removerPagamento(self, p: Pagamento):
        self.__pagamentos.remove(p)

    def valorTotal(self) -> float:
        return self.__valor + sum(proc.custo for proc in self.__procedimentos)

    def valorPago(self) -> float:
        return sum(pag.valor_pago for pag in self.__pagamentos)

    def valorRestante(self) -> float:
        return self.valorTotal() - self.valorPago()

    def atualizar(self, tipo_atendimento: TipoAtendimento, data_atendimento: date, hora_marcada: time, valor_base: float):
        hoje = date.today()
        inicio_dt = datetime.combine(hoje, hora_marcada)
        fim_dt = inicio_dt + timedelta(minutes=30)
        hora_fim_calculada = fim_dt.time()

        if hora_marcada < self.__clinica.hora_abertura or hora_fim_calculada > self.__clinica.hora_fechamento:
            raise ValueError(f"A consulta ({hora_marcada.strftime('%H:%M')} às {hora_fim_calculada.strftime('%H:%M')}) ultrapassa o horário de funcionamento da clínica.")

        self.__tipo_atendimento = tipo_atendimento
        self.__data_atendimento = data_atendimento
        self.__hora_inicio = hora_marcada
        self.__hora_fim = hora_fim_calculada
        self.__valor = valor_base

    def relink_referencias(self, clinica: Clinica, paciente: Paciente, profissional: Profissional, tipo_atendimento: TipoAtendimento):
        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__tipo_atendimento = tipo_atendimento
