from datetime import datetime
from view.tela_generica import TelaGenerica

class TelaAtendimento(TelaGenerica):
    def tela_opcoes(self) -> int:
        print("\n--- ATENDIMENTOS ---")
        print("1 - Agendar Atendimento")
        print("2 - Listar Atendimentos")
        print("3 - Cancelar/Excluir Atendimento")
        print("0 - Voltar")
        return self.ler_inteiro("Escolha: ", [0, 1, 2, 3])

    def pegar_dados_atendimento(self) -> dict:
        codigo = self.ler_inteiro("Código do Atendimento (número): ")
        while True:
            try:
                data_str = input("Data do Atendimento (DD/MM/AAAA): ")
                hora_inicio_str = input("Hora da Consulta (HH:MM): ") 
                valor_str = input("Valor Base (R$): ")
                
                data_atendimento = datetime.strptime(data_str, "%d/%m/%Y").date()
                hora_inicio = datetime.strptime(hora_inicio_str, "%H:%M").time()
                valor_base = float(valor_str.replace(",", "."))
                break
            except ValueError:
                print("Erro: Formato inválido.")
                
        return {
            "codigo": codigo, 
            "data": data_atendimento, 
            "hora_inicio": hora_inicio, 
            "valor_base": valor_base
        }
        
    def selecionar_paciente(self, pacientes: list):
        print("\n--- SELECIONE O PACIENTE ---")
        for i, p in enumerate(pacientes): print(f"{i} - {p.nome} (CPF: {p.cpf})")
        return pacientes[self.ler_inteiro("Número do paciente: ", list(range(len(pacientes))))]

    def selecionar_profissional(self, profissionais: list):
        print("\n--- SELECIONE O MÉDICO ---")
        for i, p in enumerate(profissionais): print(f"{i} - Dr(a). {p.nome} ({p.especialidade})")
        return profissionais[self.ler_inteiro("Número do médico: ", list(range(len(profissionais))))]

    def selecionar_clinica(self, clinicas: list):
        print("\n--- SELECIONE A CLÍNICA ---")
        for i, c in enumerate(clinicas): print(f"{i} - {c.nome}")
        return clinicas[self.ler_inteiro("Número da clínica: ", list(range(len(clinicas))))]