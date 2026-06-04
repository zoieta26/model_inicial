import pickle

class DAO:
    def __init__(self):
        # Nome do ficheiro que será criado automaticamente na pasta do projeto
        self.__datasource = "dados_sistema.pkl"

    def salvar(self, dados):
        # Abre o ficheiro em modo 'wb' (Write Binary) para escrever os objetos
        with open(self.__datasource, 'wb') as arquivo:
            pickle.dump(dados, arquivo)

    def carregar(self):
        try:
            # Tenta abrir o ficheiro em modo 'rb' (Read Binary)
            with open(self.__datasource, 'rb') as arquivo:
                return pickle.load(arquivo)
        except FileNotFoundError:
            # Se for a primeira vez que o sistema corre e o ficheiro ainda não existir, 
            # devolve um dicionário com listas vazias para não dar erro.
            return {"pacientes": [], "profissionais": [], "clinicas": [], "atendimentos": []}