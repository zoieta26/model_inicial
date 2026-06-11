from view.tela_generica import TelaGenerica

class TelaRelatorio(TelaGenerica):
    def tela_opcoes(self) -> int:
        print("\n--- RELATÓRIOS ---")
        print("1 - Clínicas com mais atendimentos")
        print("0 - Voltar")
        return self.ler_inteiro("Escolha: ", [0, 1])