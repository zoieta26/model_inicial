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
    def pacientes(self): 
        return self.__pacientes
    
    @property
    def profissionais(self): 
        return self.__profissionais

    def abrir_tela(self):
        opcoes = {
            1: self.incluir_paciente, 2: self.listar_pacientes,
            3: self.incluir_profissional, 4: self.listar_profissionais,
            5: self.excluir_paciente, 6: self.excluir_profissional
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0: break 
            else: opcoes[opcao]()

    def incluir_paciente(self):
        dados = self.__tela.pegar_dados_base()
        paciente = Paciente(dados["nome"], dados["celular"], dados["cpf"], dados["data_nascimento"])
        self.__pacientes.append(paciente)
        self.__tela.mostrar_mensagem("Paciente cadastrado com sucesso!")

    def listar_pacientes(self):
        if not self.__pacientes:
            self.__tela.mostrar_mensagem("Nenhum paciente cadastrado.")
            return
        for p in self.__pacientes:
            self.__tela.mostrar_mensagem(f"Paciente: {p.nome} | CPF: {p.cpf} | Idade: {p.idade()} anos")

    def incluir_profissional(self):
        dados = self.__tela.pegar_dados_base()
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
            self.__tela.mostrar_mensagem(f"Profissional: {p.nome} | Esp: {p.especialidade} | Reg: {p.registro_profissional}")
    
    def excluir_paciente(self):
        self.listar_pacientes()
        if not self.__pacientes: return
        cpf = input("\nDigite o CPF do paciente que deseja excluir: ")
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                self.__pacientes.remove(paciente)
                self.__tela.mostrar_mensagem("Paciente retirado do sistema com sucesso!")
                return
        self.__tela.mostrar_mensagem("CPF não encontrado.")

    def excluir_profissional(self):
        self.listar_profissionais()
        if not self.__profissionais: return
        cpf = input("\nDigite o CPF do profissional que deseja excluir: ")
        for prof in self.__profissionais:
            if prof.cpf == cpf:
                self.__profissionais.remove(prof)
                self.__tela.mostrar_mensagem("Profissional excluído do sistema!")
                return
        self.__tela.mostrar_mensagem("CPF não encontrado.")