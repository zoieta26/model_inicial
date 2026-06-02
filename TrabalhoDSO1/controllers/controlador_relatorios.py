from view.tela_relatorio import TelaRelatorio

class ControladorRelatorios:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaRelatorio()

    def abrir_tela(self):
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0: 
                break 
            elif opcao == 1:
                # Chama a nova função real do relatório
                self.relatorio_clinicas_mais_atendimentos()

    def relatorio_clinicas_mais_atendimentos(self):
        # 1. Puxa a lista do controlador de atendimentos
        lista_atendimentos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        
        if not lista_atendimentos:
            self.__tela.mostrar_mensagem("Ainda não há atendimentos agendados no sistema.")
            return

        # 2. Faz a contagem usando um dicionário (nome_clinica: quantidade)
        contagem = {}
        for a in lista_atendimentos:
            nome = a.clinica.nome
            if nome in contagem:
                contagem[nome] += 1
            else:
                contagem[nome] = 1

        # 3. Ordena os dados (da clínica com mais atendimentos para a que tem menos)
        clinicas_ordenadas = sorted(contagem.items(), key=lambda item: item[1], reverse=True)

        # 4. Mostra o resultado bonitinho na tela
        self.__tela.mostrar_mensagem("RANKING: CLÍNICAS COM MAIS ATENDIMENTOS")
        for posicao, (nome_clinica, qtd) in enumerate(clinicas_ordenadas, start=1):
            print(f"{posicao}º Lugar -> {nome_clinica}: {qtd} atendimento(s)")