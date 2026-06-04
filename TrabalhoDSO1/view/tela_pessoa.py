from datetime import datetime
from view.tela_generica import TelaGenerica

class TelaPessoa(TelaGenerica):
    def tela_opcoes(self) -> int:
        print("\n--- PESSOAS ---")
        print("1 - Cadastrar Paciente")
        print("2 - Listar Pacientes")
        print("3 - Editar Paciente")     # <-- NOVO
        print("4 - Excluir Paciente")    
        print("5 - Cadastrar Profissional")
        print("6 - Listar Profissionais")
        print("7 - Editar Profissional") # <-- NOVO
        print("8 - Excluir Profissional")
        print("0 - Voltar")
        return self.ler_inteiro("Escolha: ", [0, 1, 2, 3, 4, 5, 6, 7, 8])

    def pegar_dados_base(self) -> dict:
        nome = input("Nome: ")
        celular = input("Celular: ")
        cpf = input("CPF: ")
        while True:
            try:
                data_str = input("Data de Nascimento (DD/MM/AAAA): ")
                data_nasc = datetime.strptime(data_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print("Formato inválido.")
        return {"nome": nome, "celular": celular, "cpf": cpf, "data_nascimento": data_nasc}

    def pegar_dados_profissional(self) -> dict:
        esp = input("Especialidade: ")
        reg = input("Registro (CRM/COREN): ")
        return {"especialidade": esp, "registro": reg}