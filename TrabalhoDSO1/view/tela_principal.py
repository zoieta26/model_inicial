from view.tela_generica import TelaGenerica

class TelaPrincipal(TelaGenerica):
    def tela_opcoes(self) -> int:
        print("\n" + "="*30)
        print("SISTEMA DE CLÍNICAS")
        print("1 - Módulo Pessoas")
        print("2 - Módulo Clínicas")
        print("3 - Módulo Atendimentos") 
        print("4 - Módulo Relatórios")   
        print("0 - Sair")
        return self.ler_inteiro("Escolha uma opção: ", [0, 1, 2, 3, 4])