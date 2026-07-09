from view.tela_relatorio import TelaRelatorio

class ControladorRelatorios:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaRelatorio()

    def abrir_tela(self):
        opcoes = {
            "Clínicas com mais atendimentos": self.relatorio_clinicas_mais_atendimentos,
            "Relatório Financeiro (Faturação por Clínica)": self.relatorio_faturamento,
            "Procedimentos mais realizados": self.relatorio_procedimentos_mais_realizados,
            "Atendimentos mais caros e mais baratos": self.relatorio_atendimentos_mais_caros_baratos,
            "Procedimentos mais caros e mais baratos": self.relatorio_procedimentos_mais_caros_baratos,
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == "Voltar":
                break
            else:
                opcoes[opcao]()

    def relatorio_clinicas_mais_atendimentos(self):
        lista_atendimentos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        if not lista_atendimentos:
            self.__tela.mostrar_mensagem("Ainda não há atendimentos agendados no sistema.")
            return

        contagem = {}
        for a in lista_atendimentos:
            nome = a.clinica.nome
            contagem[nome] = contagem.get(nome, 0) + 1

        clinicas_ordenadas = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

        linhas = [f"{pos}º Lugar -> {nome}: {qtd} atendimento(s)" for pos, (nome, qtd) in enumerate(clinicas_ordenadas, start=1)]
        self.__tela.mostrar_lista("Ranking: Clínicas com Mais Atendimentos", linhas)

    def relatorio_faturamento(self):
        lista_atendimentos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        if not lista_atendimentos:
            self.__tela.mostrar_mensagem("Ainda não há faturação registada.")
            return

        faturacao = {}

        for a in lista_atendimentos:
            nome = a.clinica.nome
            valor_recebido = a.valorPago()
            if valor_recebido > 0:
                faturacao[nome] = faturacao.get(nome, 0.0) + valor_recebido

        if not faturacao:
            self.__tela.mostrar_mensagem("Nenhum atendimento foi finalizado/pago ainda.")
            return

        faturacao_ordenada = sorted(faturacao.items(), key=lambda item: item[1], reverse=True)

        linhas = [f"{pos}º Lugar -> {nome}: R$ {total:.2f}" for pos, (nome, total) in enumerate(faturacao_ordenada, start=1)]
        self.__tela.mostrar_lista("Relatório Financeiro: Faturação Total por Clínica", linhas)

    def relatorio_procedimentos_mais_realizados(self):
        lista_atendimentos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        if not lista_atendimentos:
            self.__tela.mostrar_mensagem("Ainda não há atendimentos agendados no sistema.")
            return

        contagem = {}
        for a in lista_atendimentos:
            for proc in a.procedimentos:
                contagem[proc.descricao] = contagem.get(proc.descricao, 0) + 1

        if not contagem:
            self.__tela.mostrar_mensagem("Nenhum procedimento foi registado ainda.")
            return

        procedimentos_ordenados = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

        linhas = [f"{pos}º Lugar -> {desc}: {qtd} vez(es)" for pos, (desc, qtd) in enumerate(procedimentos_ordenados, start=1)]
        self.__tela.mostrar_lista("Ranking: Procedimentos Mais Realizados", linhas)

    def relatorio_atendimentos_mais_caros_baratos(self):
        lista_atendimentos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        if not lista_atendimentos:
            self.__tela.mostrar_mensagem("Ainda não há atendimentos agendados no sistema.")
            return

        atendimentos_ordenados = sorted(lista_atendimentos, key=lambda a: a.valorTotal(), reverse=True)

        linhas = [
            f"{pos}º Lugar -> Cód: {a.codigo} | Paciente: {a.paciente.nome} | Médico: {a.profissional.nome} | Valor Total: R$ {a.valorTotal():.2f}"
            for pos, a in enumerate(atendimentos_ordenados, start=1)
        ]
        self.__tela.mostrar_lista("Ranking: Atendimentos do Mais Caro ao Mais Barato", linhas)

    def relatorio_procedimentos_mais_caros_baratos(self):
        lista_atendimentos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        if not lista_atendimentos:
            self.__tela.mostrar_mensagem("Ainda não há atendimentos agendados no sistema.")
            return

        procedimentos_realizados = []
        for a in lista_atendimentos:
            for proc in a.procedimentos:
                procedimentos_realizados.append((a, proc))

        if not procedimentos_realizados:
            self.__tela.mostrar_mensagem("Nenhum procedimento foi registado ainda.")
            return

        procedimentos_ordenados = sorted(procedimentos_realizados, key=lambda item: item[1].custo, reverse=True)

        linhas = [
            f"{pos}º Lugar -> {proc.descricao} | Atendimento Cód: {a.codigo} | Responsável: Dr(a). {proc.responsavel.nome} | Custo: R$ {proc.custo:.2f}"
            for pos, (a, proc) in enumerate(procedimentos_ordenados, start=1)
        ]
        self.__tela.mostrar_lista("Ranking: Procedimentos do Mais Caro ao Mais Barato", linhas)
