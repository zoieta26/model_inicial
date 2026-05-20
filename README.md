# model_inicial

#1. Documento de Divisão de Tarefas (Salvar como PDF) 

# Copie o texto abaixo, preencha o nome do seu colega, cole em um editor de texto (como Word ou Google Docs) e exporte como PDF. Ele tem o tamanho ideal para dar no máximo 1 página.  

# INE5605 - Desenvolvimento de Sistemas Orientados a Objetos I Curso: Sistemas de Informação - UFSC Equipe: Lucas Feitor e Pedro Araujo Divisão de Atividades - Trabalho 1 (Sistema de Clínicas)

# Este documento formaliza a divisão de tarefas entre os dois membros da equipe para o desenvolvimento do sistema de gerenciamento de clínicas. A distribuição foi pensada para manter um equilíbrio na carga de trabalho e garantir a correta aplicação do padrão de   arquitetura MVC (Model-View-Controller) exigido na disciplina.

# Lucas Feitor:Model (Entidades): Implementação completa do pacote Model, garantindo o encapsulamento (getters/setters), heranças, classes abstratas e as lógicas de negócio internas (cálculo de idade, valor total e restante).Controladores Core: Desenvolvimento do ControladorAtendimentos (com validação das regras de negócio de idade e horário) e do ControladorPessoas (pacientes e profissionais).Infraestrutura: Criação do repositório no Git e gerenciamento inicial dos commits e versionamento do código.

# Pedro Araujo :View (Telas): Implementação de todas as classes de interface com o usuário (TelaPrincipal, TelaPessoa, TelaClinica, TelaAtendimento), centralizando os blocos try-except para tratamento de exceções de input (ex: ValueError).Controladores de Suporte e Fluxo: 

# Desenvolvimento do ControladorPrincipal (menu raiz), ControladorClinicas (com a lógica de vinculação de profissionais) e emissão de todos os Relatórios.Modelagem: Finalização e exportação do Diagrama de Classes UML do sistema completo para a entrega final.2. A Imagem do 

# Diagrama de Classes (Somente Model)Para o dia 22/05, você não deve entregar o diagrama do MVC completo. O PDF pede explicitamente "uma figura com o diagrama de classes somente das entidades (Model)".  
# O que você deve fazer:

# Abra o seu arquivo diagrama_classes.drawio.html.O diagrama que você já fez lá tem exatamente as entidades do Model.Exporte essa visualização como uma imagem (.png ou .jpg) e anexe na sua entrega.3. Código-Fonte em Python (Somente Model)O PDF pede o "Código-fonte orientado a objetos em Python somente com a implementação das entidades (Model)".  

# Aqui está o arquivo model.py final, unindo as classes que criamos com o encapsulamento adequado (Getters e Setters) e o uso do módulo abc. Você só precisa entregar este código na sexta-feira. Nenhuma View ou Controller deve ir nesse arquivo agora.
