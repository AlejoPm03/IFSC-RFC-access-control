# Funcionamento do Cliente de Controle de Acesso

O cliente de controle de acesso é a parte do sistema que permite aos usuários interagir com as portas e o servidor central para autenticar-se, registrar-se, fazer logout e solicitar acesso às portas controladas.

## Visão Geral

O cliente é uma aplicação que roda em terminais próximos às portas controladas. Ele permite que os usuários realizem ações como fazer login, registrar-se, fazer logout e solicitar acesso a uma porta específica. O cliente se comunica com o servidor central para verificar a autenticidade do usuário e obter autorização para acessar uma porta.

## Funcionamento Detalhado

### Inicialização

- O cliente é inicializado com as seguintes informações:
  - Endereço IP e porta do servidor central.
  - Tempo limite de resposta em segundos (padrão: 5 segundos).
  - Um ID para identificar a porta onde o cliente está instalado.

### Execução

- O cliente entra em um loop onde ele exibe um menu de opções para o usuário escolher o que deseja fazer.
- As opções incluem:
  - Fazer login.
  - Registrar-se como novo usuário.
  - Fazer logout.
  - Solicitar acesso a uma porta.
  - Sair do cliente.

### Menu de Opções

- O cliente exibe um menu de opções para o usuário com base em sua escolha.
- Dependendo da opção escolhida, o cliente chama a função correspondente para executar a ação.

### Fazer Login

- Quando o usuário escolhe fazer login, o cliente solicita que ele insira seu nome de usuário e senha.
- O cliente cria uma mensagem de login e envia-a para o servidor central.
- O servidor central verifica as credenciais do usuário e envia uma resposta ao cliente.
- Se o login for bem-sucedido, o cliente registra o usuário como logado e pode continuar a realizar outras ações.
- Se o login falhar, o cliente exibe uma mensagem de erro.

### Registrar-se

- Quando o usuário escolhe registrar-se como novo usuário, o cliente verifica se ele já está logado.
- Se não estiver logado, o cliente não permite o registro e exibe uma mensagem de erro.
- Se o usuário estiver logado, o cliente solicita que ele insira um novo nome de usuário e senha.
- O cliente cria uma mensagem de registro e a envia para o servidor central.
- O servidor central verifica se o usuário tem permissão para registrar novos usuários e, em seguida, cria o novo usuário se possível.
- O cliente recebe uma resposta do servidor informando se o registro foi bem-sucedido ou não.

### Fazer Logout

- O cliente permite que o usuário faça logout, o que significa que ele perde seu acesso atual.
- O cliente define o usuário como um "convidado" e permite que ele realize ações limitadas.

### Solicitar Acesso

- Quando o usuário escolhe solicitar acesso a uma porta, o cliente verifica se ele está logado.
- Se não estiver logado, o cliente não permite a solicitação e exibe uma mensagem de erro.
- Se o usuário estiver logado, o cliente cria uma mensagem de solicitação de acesso e a envia para o servidor central.
- O servidor central verifica as credenciais do usuário e a porta específica e envia uma resposta ao cliente.
- Se o acesso for autorizado, o cliente recebe uma mensagem de sucesso; caso contrário, ele recebe uma mensagem de negação.

### Encerramento

- O cliente permite que o usuário saia do programa a qualquer momento escolhendo a opção "Sair".
- Quando o usuário sai, o cliente fecha sua execução.

## Para Pessoas Não Familiarizadas com o Projeto

Se você não estiver familiarizado com o projeto, aqui está uma explicação simplificada:

Imagine um sistema de controle de acesso em que várias portas estão trancadas e protegidas. O cliente é como um aplicativo que você encontra próximo a cada porta, e ele permite que você faça o seguinte:

- Faça login com seu nome de usuário e senha para desbloquear a porta e entrar.
- Registre-se como novo usuário (somente se você já estiver logado).
- Faça logout para sair e bloquear a porta.
- Solicite acesso a uma porta específica.

O cliente se comunica com o servidor central para verificar suas credenciais e obter autorização para acessar a porta. O servidor central é o cérebro do sistema que decide quem pode entrar e quem não pode. Ele também mantém registros de todas as ações dos usuários.