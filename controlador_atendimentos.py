from datetime import datetime, date, timedelta
from model.atendimento import Atendimento
from view.tela_atendimento import TelaAtendimento

class ControladorAtendimentos:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaAtendimento()
        self.__atendimentos = []
    
    @property
    def atendimentos(self): 
        return self.__atendimentos

    def abrir_tela(self):
        opcoes = {1: self.agendar_atendimento, 2: self.listar_atendimentos, 3: self.excluir_atendimento}
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0: break 
            else: opcoes[opcao]()

    def agendar_atendimento(self):
        pacientes = self.__ctrl_principal.ctrl_pessoas.pacientes
        profissionais = self.__ctrl_principal.ctrl_pessoas.profissionais
        clinicas = self.__ctrl_principal.ctrl_clinicas.get_clinicas()

        if not pacientes or not clinicas or not profissionais:
            self.__tela.mostrar_mensagem("Erro: É necessário ter pelo menos 1 paciente, 1 médico e 1 clínica cadastrados!")
            return

        paciente_escolhido = self.__tela.selecionar_paciente(pacientes)
        profissional_escolhido = self.__tela.selecionar_profissional(profissionais)
        clinica_escolhida = self.__tela.selecionar_clinica(clinicas)
        dados = self.__tela.pegar_dados_atendimento()

        dummy_dt = datetime.combine(date.today(), dados["hora_inicio"])
        nova_hora_fim = (dummy_dt + timedelta(minutes=30)).time()

        for a in self.__atendimentos:
            if a.data_atendimento == dados["data"] and a.profissional.cpf == profissional_escolhido.cpf:
                if dados["hora_inicio"] < a.hora_fim and nova_hora_fim > a.hora_inicio:
                    self.__tela.mostrar_mensagem(f"ERRO DE AGENDA: Dr(a). {profissional_escolhido.nome} já tem consulta das {a.hora_inicio.strftime('%H:%M')} às {a.hora_fim.strftime('%H:%M')}.")
                    return 

        try:
            novo_atendimento = Atendimento(
                dados["codigo"], dados["data"], dados["hora_inicio"], 
                clinica_escolhida, paciente_escolhido, profissional_escolhido, dados["valor_base"]
            )
            self.__atendimentos.append(novo_atendimento)
            self.__tela.mostrar_mensagem("Atendimento agendado com sucesso (30 minutos reservados)!")
            
        except ValueError as e:
            self.__tela.mostrar_mensagem(f"ATENÇÃO - Regra de Negócio: {e}")

    def listar_atendimentos(self):
        if not self.__atendimentos:
            self.__tela.mostrar_mensagem("Nenhum atendimento agendado.")
            return
            
        for a in self.__atendimentos:
            data_formatada = a.data_atendimento.strftime("%d/%m/%Y") 
            h_inicio = a.hora_inicio.strftime("%H:%M")
            h_fim = a.hora_fim.strftime("%H:%M")
            self.__tela.mostrar_mensagem(
                f"Cód: {a.codigo} | Data: {data_formatada} ({h_inicio} às {h_fim}) | Paciente: {a.paciente.nome} | Médico: {a.profissional.nome}"
            )

    def excluir_atendimento(self):
        self.listar_atendimentos()
        if not self.__atendimentos: return
            
        codigo = self.__tela.ler_inteiro("\nDigite o CÓDIGO do atendimento que deseja cancelar: ")
        for atendimento in self.__atendimentos:
            if atendimento.codigo == codigo:
                self.__atendimentos.remove(atendimento)
                self.__tela.mostrar_mensagem("Atendimento cancelado! O horário do médico foi liberado na agenda.")
                return
        self.__tela.mostrar_mensagem("Código não encontrado.")