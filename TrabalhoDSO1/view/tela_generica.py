class TelaGenerica:
    def mostrar_mensagem(self, msg: str):
        print(f"\n>>> {msg} <<<")

    def ler_inteiro(self, mensagem: str, opcoes_validas: list = None) -> int:
        while True:
            try:
                valor = int(input(mensagem))
                if opcoes_validas and valor not in opcoes_validas:
                    print("Erro: Opção inválida.")
                    continue
                return valor
            except ValueError:
                print("Erro: Digite um número inteiro válido.")