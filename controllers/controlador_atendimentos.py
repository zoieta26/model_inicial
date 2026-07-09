from datetime import datetime, date, timedelta
from model.atendimento import Atendimento
from view.tela_atendimento import TelaAtendimento
from model.procedimento import Procedimento
from model.pagamento import PagamentoDinheiro, PagamentoPix, PagamentoCartao
from dao.atendimento_dao import AtendimentoDAO

class ControladorAtendimentos:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaAtendimento()
        self.__dao = AtendimentoDAO()
        self.__atendimentos = self.__dao.listar()
        self.__relink_referencias()

    def __relink_referencias(self):
        clinicas = {c.codigo: c for c in self.__ctrl_principal.ctrl_clinicas.get_clinicas()}
        pacientes = {p.cpf: p for p in self.__ctrl_principal.ctrl_pessoas.pacientes}
        profissionais = {p.cpf: p for p in self.__ctrl_principal.ctrl_pessoas.profissionais}
        tipos = {t.codigo: t for t in self.__ctrl_principal.ctrl_tipos_atendimento.get_tipos()}

        for a in self.__atendimentos:
            clinica = clinicas.get(a.clinica.codigo, a.clinica)
            paciente = pacientes.get(a.paciente.cpf, a.paciente)
            profissional = profissionais.get(a.profissional.cpf, a.profissional)
            tipo = tipos.get(a.tipo_atendimento.codigo, a.tipo_atendimento)
            a.relink_referencias(clinica, paciente, profissional, tipo)

            for proc in a.procedimentos:
                proc.responsavel = profissionais.get(proc.responsavel.cpf, proc.responsavel)
            for pag in a.pagamentos:
                pag.paciente = pacientes.get(pag.paciente.cpf, pag.paciente)

    @property
    def atendimentos(self):
        return self.__atendimentos

    def abrir_tela(self):
        opcoes = {
            "Agendar Atendimento": self.agendar_atendimento,
            "Listar Atendimentos": self.listar_atendimentos,
            "Editar Atendimento": self.editar_atendimento,
            "Cancelar/Excluir Atendimento": self.excluir_atendimento,
            "Adicionar Procedimento": self.adicionar_procedimento,
            "Editar Procedimento": self.editar_procedimento,
            "Excluir Procedimento": self.excluir_procedimento,
            "Registrar Pagamento": self.registrar_pagamento,
            "Editar Pagamento": self.editar_pagamento,
            "Excluir Pagamento": self.excluir_pagamento,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == "Voltar": break
            else: opcoes[opcao]()

    @staticmethod
    def _calcular_hora_fim(hora_inicio):
        dummy_dt = datetime.combine(date.today(), hora_inicio)
        return (dummy_dt + timedelta(minutes=30)).time()

    def _verificar_conflito(self, data, hora_inicio, hora_fim, profissional, ignorar_codigo=None):
        for a in self.__atendimentos:
            if a.codigo == ignorar_codigo:
                continue
            if a.data_atendimento == data and a.profissional.cpf == profissional.cpf:
                if hora_inicio < a.hora_fim and hora_fim > a.hora_inicio:
                    return a
        return None

    def _linha_atendimento(self, a: Atendimento) -> str:
        data_formatada = a.data_atendimento.strftime("%d/%m/%Y")
        h_inicio = a.hora_inicio.strftime("%H:%M")
        h_fim = a.hora_fim.strftime("%H:%M")
        return (
            f"Cód: {a.codigo} | Tipo: {a.tipo_atendimento.descricao} | Data: {data_formatada} ({h_inicio} às {h_fim}) | "
            f"Paciente: {a.paciente.nome} | Médico: {a.profissional.nome}\n"
            f"    Valor Total: R$ {a.valorTotal():.2f} | Pago: R$ {a.valorPago():.2f} | Restante: R$ {a.valorRestante():.2f}"
        )

    def _linha_atendimento_compacta(self, a: Atendimento) -> str:
        data_formatada = a.data_atendimento.strftime("%d/%m/%Y")
        h_inicio = a.hora_inicio.strftime("%H:%M")
        return (
            f"Cód: {a.codigo} | {data_formatada} {h_inicio} | {a.paciente.nome} | Dr(a). {a.profissional.nome} | "
            f"Total: R$ {a.valorTotal():.2f} | Restante: R$ {a.valorRestante():.2f}"
        )

    def _selecionar_atendimento(self):
        if not self.__atendimentos:
            self.__tela.mostrar_mensagem("Nenhum atendimento agendado.")
            return None
        return self.__tela.selecionar_da_lista(
            "Selecione o Atendimento", [self._linha_atendimento_compacta(a) for a in self.__atendimentos], self.__atendimentos
        )

    def agendar_atendimento(self):
        pacientes = self.__ctrl_principal.ctrl_pessoas.pacientes
        profissionais = self.__ctrl_principal.ctrl_pessoas.profissionais
        clinicas = self.__ctrl_principal.ctrl_clinicas.get_clinicas()
        tipos = self.__ctrl_principal.ctrl_tipos_atendimento.get_tipos()

        if not pacientes or not clinicas or not profissionais or not tipos:
            self.__tela.mostrar_erro("É necessário ter pelo menos 1 paciente, 1 médico, 1 clínica e 1 tipo de atendimento cadastrados!")
            return

        paciente_escolhido = self.__tela.selecionar_da_lista(
            "Selecione o Paciente", [f"{p.nome} (CPF: {p.cpf})" for p in pacientes], pacientes
        )
        if paciente_escolhido is None: return

        profissional_escolhido = self.__tela.selecionar_da_lista(
            "Selecione o Médico", [f"Dr(a). {p.nome} ({p.especialidade})" for p in profissionais], profissionais
        )
        if profissional_escolhido is None: return

        clinica_escolhida = self.__tela.selecionar_da_lista(
            "Selecione a Clínica", [c.nome for c in clinicas], clinicas
        )
        if clinica_escolhida is None: return

        tipo_escolhido = self.__tela.selecionar_da_lista(
            "Selecione o Tipo de Atendimento", [t.descricao for t in tipos], tipos
        )
        if tipo_escolhido is None: return

        dados = self.__tela.pegar_dados_atendimento()
        if dados is None: return

        nova_hora_fim = self._calcular_hora_fim(dados["hora_inicio"])

        conflito = self._verificar_conflito(dados["data"], dados["hora_inicio"], nova_hora_fim, profissional_escolhido)
        if conflito:
            self.__tela.mostrar_erro(f"ERRO DE AGENDA: Dr(a). {profissional_escolhido.nome} já tem consulta das {conflito.hora_inicio.strftime('%H:%M')} às {conflito.hora_fim.strftime('%H:%M')}.")
            return

        try:
            novo_atendimento = Atendimento(
                dados["codigo"], dados["data"], dados["hora_inicio"],
                clinica_escolhida, paciente_escolhido, profissional_escolhido, tipo_escolhido, dados["valor_base"]
            )
            self.__dao.incluir(novo_atendimento)
            self.__tela.mostrar_mensagem("Atendimento agendado com sucesso (30 minutos reservados)!")

        except ValueError as e:
            self.__tela.mostrar_erro(f"Regra de Negócio: {e}")

    def listar_atendimentos(self):
        self.__tela.mostrar_lista("Atendimentos Agendados", [self._linha_atendimento(a) for a in self.__atendimentos])

    def editar_atendimento(self):
        a = self._selecionar_atendimento()
        if not a: return

        tipos = self.__ctrl_principal.ctrl_tipos_atendimento.get_tipos()
        if not tipos:
            self.__tela.mostrar_erro("É necessário ter pelo menos 1 tipo de atendimento cadastrado!")
            return

        tipo_escolhido = self.__tela.selecionar_da_lista(
            "Selecione o Tipo de Atendimento", [t.descricao for t in tipos], tipos
        )
        if tipo_escolhido is None: return

        dados = self.__tela.pegar_dados_edicao_atendimento(
            a.data_atendimento.strftime("%d/%m/%Y"), a.hora_inicio.strftime("%H:%M"), f"{a.valor_base:.2f}"
        )
        if dados is None: return

        nova_hora_fim = self._calcular_hora_fim(dados["hora_inicio"])
        conflito = self._verificar_conflito(dados["data"], dados["hora_inicio"], nova_hora_fim, a.profissional, ignorar_codigo=a.codigo)
        if conflito:
            self.__tela.mostrar_erro(f"ERRO DE AGENDA: Dr(a). {a.profissional.nome} já tem consulta das {conflito.hora_inicio.strftime('%H:%M')} às {conflito.hora_fim.strftime('%H:%M')}.")
            return

        try:
            a.atualizar(tipo_escolhido, dados["data"], dados["hora_inicio"], dados["valor_base"])
            self.__dao.alterar(a)
            self.__tela.mostrar_mensagem("Atendimento atualizado com sucesso!")
        except ValueError as e:
            self.__tela.mostrar_erro(f"Regra de Negócio: {e}")

    def excluir_atendimento(self):
        a = self._selecionar_atendimento()
        if not a: return

        self.__dao.excluir(a)
        self.__tela.mostrar_mensagem("Atendimento cancelado! O horário do médico foi liberado na agenda.")

    def adicionar_procedimento(self):
        a = self._selecionar_atendimento()
        if not a: return

        while True:
            dados_proc = self.__tela.pegar_dados_procedimento()
            if dados_proc is None: return

            procedimento = Procedimento(dados_proc["codigo"], dados_proc["descricao"], dados_proc["custo"], a.profissional)
            a.adicionarProcedimento(procedimento)
            self.__dao.alterar(a)
            self.__tela.mostrar_mensagem(f"Procedimento adicionado! Novo valor total do atendimento: R$ {a.valorTotal():.2f}")

            if not self.__tela.confirmar("Deseja adicionar outro procedimento a este atendimento?"):
                break

    def _linha_procedimento(self, p: Procedimento) -> str:
        return f"Cód: {p.codigo} | {p.descricao} | R$ {p.custo:.2f}"

    def editar_procedimento(self):
        a = self._selecionar_atendimento()
        if not a: return

        if not a.procedimentos:
            self.__tela.mostrar_mensagem("Este atendimento não possui procedimentos registados.")
            return

        procedimento = self.__tela.selecionar_da_lista(
            "Selecione o Procedimento", [self._linha_procedimento(p) for p in a.procedimentos], a.procedimentos
        )
        if not procedimento: return

        dados = self.__tela.pegar_dados_edicao_procedimento(procedimento.descricao, procedimento.custo)
        if dados is None: return

        procedimento.descricao = dados["descricao"]
        procedimento.custo = dados["custo"]
        self.__dao.alterar(a)
        self.__tela.mostrar_mensagem(f"Procedimento atualizado! Novo valor total do atendimento: R$ {a.valorTotal():.2f}")

    def excluir_procedimento(self):
        a = self._selecionar_atendimento()
        if not a: return

        if not a.procedimentos:
            self.__tela.mostrar_mensagem("Este atendimento não possui procedimentos registados.")
            return

        procedimento = self.__tela.selecionar_da_lista(
            "Selecione o Procedimento", [self._linha_procedimento(p) for p in a.procedimentos], a.procedimentos
        )
        if not procedimento: return

        a.removerProcedimento(procedimento)
        self.__dao.alterar(a)
        self.__tela.mostrar_mensagem(f"Procedimento removido! Novo valor total do atendimento: R$ {a.valorTotal():.2f}")

    def registrar_pagamento(self):
        a = self._selecionar_atendimento()
        if not a: return

        if a.valorRestante() <= 0:
            self.__tela.mostrar_mensagem("Este atendimento já está totalmente pago.")
            return

        dados_pag = self.__tela.pegar_dados_pagamento(a.valorTotal(), a.valorPago(), a.valorRestante())
        if dados_pag is None: return

        try:
            if dados_pag["tipo"] == 1:
                pagamento = PagamentoDinheiro(dados_pag["codigo"], date.today(), dados_pag["valor"], a, a.paciente)
            elif dados_pag["tipo"] == 2:
                pagamento = PagamentoPix(dados_pag["codigo"], date.today(), dados_pag["valor"], a, a.paciente, dados_pag["cpf_pagador"])
            elif dados_pag["tipo"] == 3:
                pagamento = PagamentoCartao(dados_pag["codigo"], date.today(), dados_pag["valor"], a, a.paciente, dados_pag["numero_cartao"], dados_pag["bandeira"])
        except ValueError as e:
            self.__tela.mostrar_erro(f"Regra de Negócio: {e}")
            return

        a.adicionarPagamento(pagamento)
        self.__dao.alterar(a)

        if a.valorRestante() <= 0:
            self.__tela.mostrar_mensagem(f"Pagamento registado! Atendimento totalmente pago (R$ {a.valorTotal():.2f}).")
        else:
            self.__tela.mostrar_mensagem(f"Pagamento parcial registado! Restante: R$ {a.valorRestante():.2f}")

    def _linha_pagamento(self, p) -> str:
        data_formatada = p.data_pagamento.strftime("%d/%m/%Y")
        return f"Cód: {p.codigo} | {p.modalidade()} | R$ {p.valor_pago:.2f} | {data_formatada}"

    def editar_pagamento(self):
        a = self._selecionar_atendimento()
        if not a: return

        if not a.pagamentos:
            self.__tela.mostrar_mensagem("Este atendimento não possui pagamentos registados.")
            return

        pagamento = self.__tela.selecionar_da_lista(
            "Selecione o Pagamento", [self._linha_pagamento(p) for p in a.pagamentos], a.pagamentos
        )
        if not pagamento: return

        novo_valor = self.__tela.pegar_novo_valor_pagamento(pagamento.valor_pago)
        if novo_valor is None: return

        try:
            pagamento.valor_pago = novo_valor
            self.__dao.alterar(a)
            self.__tela.mostrar_mensagem(f"Pagamento atualizado! Novo restante do atendimento: R$ {a.valorRestante():.2f}")
        except ValueError as e:
            self.__tela.mostrar_erro(f"Regra de Negócio: {e}")

    def excluir_pagamento(self):
        a = self._selecionar_atendimento()
        if not a: return

        if not a.pagamentos:
            self.__tela.mostrar_mensagem("Este atendimento não possui pagamentos registados.")
            return

        pagamento = self.__tela.selecionar_da_lista(
            "Selecione o Pagamento", [self._linha_pagamento(p) for p in a.pagamentos], a.pagamentos
        )
        if not pagamento: return

        a.removerPagamento(pagamento)
        self.__dao.alterar(a)
        self.__tela.mostrar_mensagem(f"Pagamento removido! Novo restante do atendimento: R$ {a.valorRestante():.2f}")
