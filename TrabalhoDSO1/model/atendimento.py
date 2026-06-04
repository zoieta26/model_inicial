from datetime import date, time, datetime, timedelta
from model.clinica import Clinica
from model.paciente import Paciente
from model.profissional import Profissional
from model.procedimento import Procedimento
from model.pagamento import Pagamento

class Atendimento:
    def __init__(self, codigo: int, data_atendimento: date, hora_marcada: time, clinica: Clinica, paciente: Paciente, profissional: Profissional, valor_base: float):
        
        # 1. Calcula automaticamente a hora de término (30 minutos de duração)
        hoje = date.today()
        inicio_dt = datetime.combine(hoje, hora_marcada)
        fim_dt = inicio_dt + timedelta(minutes=30)
        hora_fim_calculada = fim_dt.time()

        # Validações de Regra de Negócio
        if paciente.idade() < 18:
            raise ValueError("Pacientes menores de 18 anos não podem ser agendados sozinhos.")
        
        # Verifica se o atendimento CABE dentro do horário da clínica
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
    def paciente(self) -> Paciente: 
        return self.__paciente
    
    @property
    def profissional(self) -> Profissional: 
        return self.__profissional

    def adicionarProcedimento(self, p: Procedimento): 
        self.__procedimentos.append(p)

    def adicionarPagamento(self, p: Pagamento): 
        self.__pagamentos.append(p)

    def valorTotal(self) -> float: 
        return self.__valor + sum(proc.custo for proc in self.__procedimentos)
    
    def valorPago(self) -> float: 
        return sum(pag.valor_pago for pag in self.__pagamentos)
    
    def valorRestante(self) -> float: 
        return self.valorTotal() - self.valorPago()