from view.tela_relatorio import TelaRelatorio

class ControladorRelatorios:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaRelatorio()

    def abrir_tela(self):
        opcoes = {
            1: self.relatorio_clinicas_mais_atendimentos,
            2: self.relatorio_faturamento
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0: 
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

        self.__tela.mostrar_mensagem("RANKING: CLÍNICAS COM MAIS ATENDIMENTOS")
        for posicao, (nome_clinica, qtd) in enumerate(clinicas_ordenadas, start=1):
            print(f"{posicao}º Lugar -> {nome_clinica}: {qtd} atendimento(s)")

    def relatorio_faturamento(self):
        lista_atendimentos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        if not lista_atendimentos:
            self.__tela.mostrar_mensagem("Ainda não há faturação registada.")
            return

        faturacao = {}
        # Varre todos os atendimentos para somar os lucros
        for a in lista_atendimentos:
            nome = a.clinica.nome
            # A função valorPago() soma apenas se a consulta já foi finalizada na Opção 4
            valor_recebido = a.valorPago()
            if valor_recebido > 0:
                faturacao[nome] = faturacao.get(nome, 0.0) + valor_recebido

        if not faturacao:
            self.__tela.mostrar_mensagem("Nenhum atendimento foi finalizado/pago ainda.")
            return

        faturacao_ordenada = sorted(faturacao.items(), key=lambda item: item[1], reverse=True)

        self.__tela.mostrar_mensagem("RELATÓRIO FINANCEIRO: FATURAÇÃO TOTAL POR CLÍNICA")
        for posicao, (nome_clinica, total) in enumerate(faturacao_ordenada, start=1):
            print(f"{posicao}º Lugar -> {nome_clinica}: R$ {total:.2f}")