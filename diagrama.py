classDiagram
    class Pessoa {
        <<abstract>>
        - nome: str
        - celular: str
        - cpf: str
        - dataNascimento: date
        + idade(): int
        + tipo(): str*
    }

    class Paciente {
        + tipo(): str
    }

    class Profissional {
        - especialidade: str
        - registroProfissional: str
        + tipo(): str
    }

    class Clinica {
        - nome: str
        - cidade: str
        - descricao: str
        - horaAbertura: time
        - horaFechamento: time
        + adicionarProfissional(p)
    }

    class TipoAtendimento {
        - nome: str
        - descricao: str
    }

    class Atendimento {
        - codigo: int
        - data: date
        - horaInicio: time
        - horaFim: time
        - valor: float
        + adicionarProcedimento(p)
        + adicionarPagamento(p)
        + valorTotal(): float
        + valorPago(): float
        + valorRestante(): float
    }

    class Procedimento {
        - codigo: int
        - descricao: str
        - custo: float
    }

    class Pagamento {
        <<abstract>>
        - codigo: int
        - dataPagamento: date
        - valorPago: float
        + modalidade(): str*
        + detalhes(): str*
    }

    class PagamentoDinheiro {
        + modalidade(): str
        + detalhes(): str
    }

    class PagamentoPix {
        - cpfPagador: str
        + modalidade(): str
        + detalhes(): str
    }

    class PagamentoCartao {
        - numeroCartao: str
        - bandeira: str
        + modalidade(): str
        + detalhes(): str
    }

    %% Heranças
    Pessoa <|-- Paciente
    Pessoa <|-- Profissional
    Pagamento <|-- PagamentoDinheiro
    Pagamento <|-- PagamentoPix
    Pagamento <|-- PagamentoCartao

    %% Relacionamentos
    Clinica o-- Profissional : 1..* (Agregação)
    Atendimento *-- Procedimento : 1..* (Composição)
    Atendimento *-- Pagamento : 1..* (Composição)
    
    Atendimento --> Clinica : 1
    Atendimento --> TipoAtendimento : 1
    Atendimento --> Paciente : 1
    Atendimento --> Profissional : 1
    Procedimento --> Profissional : 1
