from model.paciente import Paciente
from model.profissional import Profissional
from view.tela_pessoa import TelaPessoa

class ControladorPessoas:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaPessoa()
        self.__pacientes = []
        self.__profissionais = []
    
    @property
    def pacientes(self): return self.__pacientes
    
    @property
    def profissionais(self): return self.__profissionais

    def abrir_tela(self):
        opcoes = {
            1: self.incluir_paciente, 2: self.listar_pacientes,
            3: self.editar_paciente, 4: self.excluir_paciente,
            5: self.incluir_profissional, 6: self.listar_profissionais,
            7: self.editar_profissional, 8: self.excluir_profissional
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0: break 
            else: opcoes[opcao]()

    # ==========================
    # LÓGICA DE PACIENTES
    # ==========================
    def incluir_paciente(self):
        dados = self.__tela.pegar_dados_base()
        
        # --- VALIDAÇÃO DE CPF ÚNICO ---
        for p in self.__pacientes:
            if p.cpf == dados["cpf"]:
                self.__tela.mostrar_mensagem("ERRO: Já existe um paciente cadastrado com este CPF!")
                return # Aborta o cadastro para não duplicar
        # ------------------------------

        paciente = Paciente(dados["nome"], dados["celular"], dados["cpf"], dados["data_nascimento"])
        self.__pacientes.append(paciente)
        self.__tela.mostrar_mensagem("Paciente cadastrado com sucesso!")

    def listar_pacientes(self):
        if not self.__pacientes:
            self.__tela.mostrar_mensagem("Nenhum paciente cadastrado.")
            return
        for p in self.__pacientes:
            self.__tela.mostrar_mensagem(f"Paciente: {p.nome} | Celular: {p.celular} | CPF: {p.cpf} | Idade: {p.idade()} anos")

    def editar_paciente(self):
        self.listar_pacientes()
        if not self.__pacientes: return
        
        cpf = input("\nDigite o CPF do paciente que deseja editar: ")
        for p in self.__pacientes:
            if p.cpf == cpf:
                self.__tela.mostrar_mensagem(f"A editar dados de: {p.nome}")
                novos_dados = self.__tela.pegar_dados_base()
                
                # Usa os Setters que já criaste no Model!
                p.nome = novos_dados["nome"]
                p.celular = novos_dados["celular"]
                # O CPF e a Data de Nascimento não devem ser alterados por questões de segurança
                
                self.__tela.mostrar_mensagem("Dados atualizados com sucesso!")
                return
        self.__tela.mostrar_mensagem("CPF não encontrado no sistema.")

    def excluir_paciente(self):
        self.listar_pacientes()
        if not self.__pacientes: return
        cpf = input("\nDigite o CPF do paciente que deseja excluir: ")
        
        # --- TRAVA DE SEGURANÇA (INTEGRIDADE REFERENCIAL) ---
        atendimentos_ativos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        for a in atendimentos_ativos:
            if a.paciente.cpf == cpf:
                self.__tela.mostrar_mensagem("ERRO: Este paciente tem consultas agendadas! Cancele o atendimento antes de o excluir.")
                return
        # ----------------------------------------------------

        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                self.__pacientes.remove(paciente)
                self.__tela.mostrar_mensagem("Paciente retirado do sistema com sucesso!")
                return
        self.__tela.mostrar_mensagem("CPF não encontrado.")

    # ==========================
    # LÓGICA DE PROFISSIONAIS
    # ==========================
    def incluir_profissional(self):
        dados = self.__tela.pegar_dados_base()
        
        # --- VALIDAÇÃO DE CPF ÚNICO ---
        for p in self.__profissionais:
            if p.cpf == dados["cpf"]:
                self.__tela.mostrar_mensagem("ERRO: Já existe um médico cadastrado com este CPF!")
                return # Aborta o cadastro
        # ------------------------------
        
        prof_dados = self.__tela.pegar_dados_profissional()
        profissional = Profissional(
            dados["nome"], dados["celular"], dados["cpf"], dados["data_nascimento"], 
            prof_dados["especialidade"], prof_dados["registro"]
        )
        self.__profissionais.append(profissional)
        self.__tela.mostrar_mensagem("Profissional cadastrado com sucesso!")
        
    def listar_profissionais(self):
        if not self.__profissionais:
            self.__tela.mostrar_mensagem("Nenhum profissional cadastrado.")
            return
        for p in self.__profissionais:
            self.__tela.mostrar_mensagem(f"Profissional: Dr(a). {p.nome} | Telemóvel: {p.celular} | Esp: {p.especialidade} | Reg: {p.registro_profissional}")

    def editar_profissional(self):
        self.listar_profissionais()
        if not self.__profissionais: return
        
        cpf = input("\nDigite o CPF do médico que deseja editar: ")
        for p in self.__profissionais:
            if p.cpf == cpf:
                self.__tela.mostrar_mensagem(f"A editar dados de: Dr(a). {p.nome}")
                novos_dados = self.__tela.pegar_dados_base()
                p.nome = novos_dados["nome"]
                p.celular = novos_dados["celular"]
                self.__tela.mostrar_mensagem("Dados do médico atualizados com sucesso!")
                return
        self.__tela.mostrar_mensagem("CPF não encontrado no sistema.")

    def excluir_profissional(self):
        self.listar_profissionais()
        if not self.__profissionais: return
        cpf = input("\nDigite o CPF do profissional que deseja excluir: ")
        
        # --- TRAVA DE SEGURANÇA PARA MÉDICOS ---
        atendimentos_ativos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        for a in atendimentos_ativos:
            if a.profissional.cpf == cpf:
                self.__tela.mostrar_mensagem("ERRO: Este médico tem consultas agendadas! Remova os atendimentos da agenda antes de o excluir.")
                return
        # ---------------------------------------

        for prof in self.__profissionais:
            if prof.cpf == cpf:
                self.__profissionais.remove(prof)
                self.__tela.mostrar_mensagem("Profissional excluído do sistema!")
                return
        self.__tela.mostrar_mensagem("CPF não encontrado.")