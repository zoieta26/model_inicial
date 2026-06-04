from datetime import datetime
from view.tela_generica import TelaGenerica

class TelaClinica(TelaGenerica):
    def tela_opcoes(self) -> int:
        print("\n--- CLÍNICAS ---")
        print("1 - Cadastrar Clínica")
        print("2 - Listar Clínicas")
        print("3 - Editar Clínica")   # <-- NOVO
        print("4 - Excluir Clínica")  # <-- Mudou para 4
        print("0 - Voltar")
        return self.ler_inteiro("Escolha: ", [0, 1, 2, 3, 4])

    def pegar_dados_clinica(self) -> dict:
        nome = input("Nome da Clínica: ")
        cidade = input("Cidade: ")
        descricao = input("Descrição (ex: Clínica Geral): ")
        
        while True:
            try:
                hora_abertura_str = input("Hora de Abertura (HH:MM): ")
                hora_fechamento_str = input("Hora de Fechamento (HH:MM): ")
                
                hora_abertura = datetime.strptime(hora_abertura_str, "%H:%M").time()
                hora_fechamento = datetime.strptime(hora_fechamento_str, "%H:%M").time()
                
                # Regra de negócio: Limite máximo até as 18h30
                hora_limite = datetime.strptime("18:30", "%H:%M").time()
                if hora_fechamento > hora_limite:
                    print("Erro: As clínicas operam no máximo até as 18:30. Digite um horário válido.")
                    continue

                break
            except ValueError:
                print("Erro: Formato de hora inválido. Por favor, use HH:MM (ex: 08:00, 18:30).")
                
        return {
            "nome": nome, 
            "cidade": cidade, 
            "descricao": descricao, 
            "hora_abertura": hora_abertura, 
            "hora_fechamento": hora_fechamento
        }