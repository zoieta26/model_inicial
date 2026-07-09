from model.paciente import Paciente
from model.profissional import Profissional
from view.tela_pessoa import TelaPessoa
from dao.paciente_dao import PacienteDAO
from dao.profissional_dao import ProfissionalDAO

class ControladorPessoas:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaPessoa()
        self.__dao_paciente = PacienteDAO()
        self.__dao_profissional = ProfissionalDAO()
        self.__pacientes = self.__dao_paciente.listar()
        self.__profissionais = self.__dao_profissional.listar()
        self.__relink_referencias()

    def __relink_referencias(self):
        clinicas = self.__ctrl_principal.ctrl_clinicas.get_clinicas()
        mapa_clinicas = {c.codigo: c for c in clinicas}

        for c in clinicas:
            c.definir_profissionais([])

        for profissional in self.__profissionais:
            clinica_real = mapa_clinicas.get(profissional.clinica.codigo)
            if clinica_real:
                profissional.clinica = clinica_real
                clinica_real.adicionar_profissional(profissional)

    @property
    def pacientes(self): return self.__pacientes

    @property
    def profissionais(self): return self.__profissionais

    def abrir_tela(self):
        opcoes = {
            "Cadastrar Paciente": self.incluir_paciente,
            "Listar Pacientes": self.listar_pacientes,
            "Editar Paciente": self.editar_paciente,
            "Excluir Paciente": self.excluir_paciente,
            "Cadastrar Profissional": self.incluir_profissional,
            "Listar Profissionais": self.listar_profissionais,
            "Editar Profissional": self.editar_profissional,
            "Excluir Profissional": self.excluir_profissional,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == "Voltar": break
            else: opcoes[opcao]()


    def incluir_paciente(self):
        dados = self.__tela.pegar_dados_base()
        if dados is None: return

        for p in self.__pacientes:
            if p.cpf == dados["cpf"]:
                self.__tela.mostrar_erro("Já existe um paciente cadastrado com este CPF!")
                return

        paciente = Paciente(dados["nome"], dados["celular"], dados["cpf"], dados["data_nascimento"])
        self.__dao_paciente.incluir(paciente)
        self.__tela.mostrar_mensagem("Paciente cadastrado com sucesso!")

    def _linha_paciente(self, p: Paciente) -> str:
        return f"{p.nome} | Celular: {p.celular} | CPF: {p.cpf} | Idade: {p.idade()} anos"

    def listar_pacientes(self):
        self.__tela.mostrar_lista("Pacientes Cadastrados", [self._linha_paciente(p) for p in self.__pacientes])

    def _selecionar_paciente(self):
        if not self.__pacientes:
            self.__tela.mostrar_mensagem("Nenhum paciente cadastrado.")
            return None
        return self.__tela.selecionar_da_lista(
            "Selecione o Paciente", [self._linha_paciente(p) for p in self.__pacientes], self.__pacientes
        )

    def editar_paciente(self):
        p = self._selecionar_paciente()
        if not p: return

        novos_dados = self.__tela.pegar_dados_edicao_pessoa(p.nome, p.celular)
        if novos_dados is None: return

        p.nome = novos_dados["nome"]
        p.celular = novos_dados["celular"]

        self.__dao_paciente.alterar(p)
        self.__tela.mostrar_mensagem("Dados atualizados com sucesso!")

    def excluir_paciente(self):
        p = self._selecionar_paciente()
        if not p: return

        atendimentos_ativos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        for a in atendimentos_ativos:
            if a.paciente.cpf == p.cpf:
                self.__tela.mostrar_erro("Este paciente tem consultas agendadas! Cancele o atendimento antes de o excluir.")
                return

        self.__dao_paciente.excluir(p)
        self.__tela.mostrar_mensagem("Paciente retirado do sistema com sucesso!")


    def incluir_profissional(self):
        clinicas = self.__ctrl_principal.ctrl_clinicas.get_clinicas()
        if not clinicas:
            self.__tela.mostrar_erro("É necessário ter pelo menos 1 clínica cadastrada antes de cadastrar um profissional!")
            return

        dados = self.__tela.pegar_dados_base()
        if dados is None: return

        for p in self.__profissionais:
            if p.cpf == dados["cpf"]:
                self.__tela.mostrar_erro("Já existe um médico cadastrado com este CPF!")
                return

        prof_dados = self.__tela.pegar_dados_profissional()
        if prof_dados is None: return

        clinica_escolhida = self.__tela.selecionar_da_lista("Selecione a Clínica", [c.nome for c in clinicas], clinicas)
        if clinica_escolhida is None: return

        profissional = Profissional(
            dados["nome"], dados["celular"], dados["cpf"], dados["data_nascimento"],
            prof_dados["especialidade"], prof_dados["registro"], clinica_escolhida
        )
        clinica_escolhida.adicionar_profissional(profissional)
        self.__dao_profissional.incluir(profissional)
        self.__tela.mostrar_mensagem(f"Profissional cadastrado com sucesso na clínica {clinica_escolhida.nome}!")

    def _linha_profissional(self, p: Profissional) -> str:
        return f"Dr(a). {p.nome} | Telemóvel: {p.celular} | Esp: {p.especialidade} | Reg: {p.registro_profissional} | Clínica: {p.clinica.nome}"

    def listar_profissionais(self):
        self.__tela.mostrar_lista("Profissionais Cadastrados", [self._linha_profissional(p) for p in self.__profissionais])

    def _selecionar_profissional(self):
        if not self.__profissionais:
            self.__tela.mostrar_mensagem("Nenhum profissional cadastrado.")
            return None
        return self.__tela.selecionar_da_lista(
            "Selecione o Profissional", [self._linha_profissional(p) for p in self.__profissionais], self.__profissionais
        )

    def editar_profissional(self):
        p = self._selecionar_profissional()
        if not p: return

        novos_dados = self.__tela.pegar_dados_edicao_pessoa(p.nome, p.celular)
        if novos_dados is None: return

        p.nome = novos_dados["nome"]
        p.celular = novos_dados["celular"]
        self.__dao_profissional.alterar(p)
        self.__tela.mostrar_mensagem("Dados do médico atualizados com sucesso!")

    def excluir_profissional(self):
        p = self._selecionar_profissional()
        if not p: return

        atendimentos_ativos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        for a in atendimentos_ativos:
            if a.profissional.cpf == p.cpf:
                self.__tela.mostrar_erro("Este médico tem consultas agendadas! Remova os atendimentos da agenda antes de o excluir.")
                return

        p.clinica.remover_profissional(p)
        self.__dao_profissional.excluir(p)
        self.__tela.mostrar_mensagem("Profissional excluído do sistema!")
