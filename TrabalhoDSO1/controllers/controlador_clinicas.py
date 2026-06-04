from model.clinica import Clinica
from view.tela_clinica import TelaClinica

class ControladorClinicas:
    def __init__(self, ctrl_principal):
        self.__ctrl_principal = ctrl_principal
        self.__tela = TelaClinica()
        self.__clinicas = []

    def abrir_tela(self):
        opcoes = {
            1: self.incluir_clinica, 2: self.listar_clinicas, 
            3: self.editar_clinica, 4: self.excluir_clinica
        }
        while True:
            opcao = self.__tela.tela_opcoes()
            if opcao == 0: break 
            else: opcoes[opcao]()

    def incluir_clinica(self):
        dados = self.__tela.pegar_dados_clinica()
        
        # --- LÓGICA DE AUTO-INCREMENTO DO CÓDIGO (ID ÚNICO) ---
        novo_codigo = 1
        if len(self.__clinicas) > 0:
            # Descobre qual é o maior código atual na lista e soma 1
            maior_codigo = max([c.codigo for c in self.__clinicas])
            novo_codigo = maior_codigo + 1
        # ----------------------------------------------------

        clinica = Clinica(
            novo_codigo, # Passando o código gerado automaticamente!
            dados["nome"], 
            dados["cidade"], 
            dados["descricao"], 
            dados["hora_abertura"], 
            dados["hora_fechamento"]
        )
        self.__clinicas.append(clinica)
        self.__tela.mostrar_mensagem(f"Clínica cadastrada com sucesso! O código gerado foi: {novo_codigo}")

    def listar_clinicas(self):
        if not self.__clinicas:
            self.__tela.mostrar_mensagem("Nenhuma clínica cadastrada.")
            return
        for c in self.__clinicas:
            abertura = c.hora_abertura.strftime("%H:%M")
            fechamento = c.hora_fechamento.strftime("%H:%M")
            # Adicionado o ID (Código) na exibição da lista
            self.__tela.mostrar_mensagem(f"Cód: {c.codigo} | Clínica: {c.nome} | Cidade: {c.cidade} | Funcionamento: {abertura} às {fechamento}")

    def editar_clinica(self):
        self.listar_clinicas()
        if not self.__clinicas: return
        
        # Agora busca pelo CÓDIGO de forma segura
        codigo = self.__tela.ler_inteiro("\nDigite o CÓDIGO da clínica que deseja editar: ")
        for c in self.__clinicas:
            if c.codigo == codigo:
                self.__tela.mostrar_mensagem(f"A editar dados de: {c.nome}")
                novos_dados = self.__tela.pegar_dados_clinica()
                
                c.nome = novos_dados["nome"]
                c.cidade = novos_dados["cidade"]
                c.descricao = novos_dados["descricao"]
                c.hora_abertura = novos_dados["hora_abertura"]
                c.hora_fechamento = novos_dados["hora_fechamento"]
                
                self.__tela.mostrar_mensagem("Dados da clínica atualizados com sucesso!")
                return
        self.__tela.mostrar_mensagem("Código não encontrado no sistema.")

    def excluir_clinica(self):
        self.listar_clinicas()
        if not self.__clinicas: return
        
        codigo = self.__tela.ler_inteiro("\nDigite o CÓDIGO da clínica que deseja excluir: ")
        
        # Trava de segurança agora compara o ID da clínica
        atendimentos_ativos = self.__ctrl_principal.ctrl_atendimentos.atendimentos
        for a in atendimentos_ativos:
            if a.clinica.codigo == codigo:
                self.__tela.mostrar_mensagem("ERRO: Esta clínica tem consultas agendadas! Remova os atendimentos antes de a excluir.")
                return

        for c in self.__clinicas:
            if c.codigo == codigo:
                self.__clinicas.remove(c)
                self.__tela.mostrar_mensagem("Clínica excluída com sucesso!")
                return
        self.__tela.mostrar_mensagem("Código não encontrado.")

    def get_clinicas(self):
        return self.__clinicas