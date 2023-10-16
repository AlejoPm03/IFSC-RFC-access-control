# Funcionamento do Servidor de Controle de Acesso

O servidor de controle de acesso é uma parte crucial do sistema de controle de acesso que gerencia a autenticação e autorização dos usuários que tentam entrar em salas controladas por portas.

## Visão Geral

O servidor é o componente central da aplicação de controle de acesso e é responsável por coordenar as interações com os clientes que estão nas portas. Ele gerencia o banco de dados de usuários, registra tentativas de acesso e decide se um usuário tem permissão para acessar uma determinada porta.

## Funcionamento Detalhado

### Inicialização

- O servidor é inicializado com as seguintes informações:
  - Endereço IP e porta na qual ele será executado.
  - Bancos de dados de usuários e portas (opcional, mas altamente recomendado).
  - A opção de habilitar ou desabilitar logs (registros de eventos).

### Execução

- O servidor entra em um loop de escuta aguardando conexões de clientes.
- Quando um cliente se conecta, o servidor cria uma nova thread para lidar com essa conexão específica. Isso permite que o servidor atenda várias solicitações de clientes simultaneamente.
- Para cada conexão, o servidor aguarda uma mensagem do cliente.

### Mensagens do Cliente

- Quando o servidor recebe uma mensagem de um cliente, ele a analisa para determinar o tipo de ação que o cliente deseja realizar.
- Os tipos de mensagem possíveis incluem:
  - Login: O cliente envia suas credenciais de autenticação (nome de usuário e senha) para verificar se ele pode acessar uma porta específica.
  - Cadastro (Signup): O cliente envia informações para criar um novo usuário no sistema (requer autenticação prévia).

### Autenticação (Login)

- Quando o cliente envia uma mensagem de login, o servidor verifica se o usuário está cadastrado no banco de dados de usuários.
- Se o usuário não for encontrado, o servidor envia uma resposta negativa para o cliente, informando que o login falhou.
- Se o usuário for encontrado, o servidor verifica se ele tem permissão para acessar a porta especificada na mensagem.
- Se o acesso for permitido, o servidor envia uma resposta positiva ao cliente, indicando que o login foi bem-sucedido.
- Caso contrário, o servidor envia uma resposta negativa, indicando que o usuário não tem permissão para acessar a porta.

### Cadastro (Signup)

- O servidor permite que um cliente crie um novo usuário no sistema somente se o cliente tiver permissão para registrar usuários. Portanto, o cliente deve fazer login primeiro.
- Após o login, o cliente envia uma mensagem de cadastro com as informações do novo usuário.
- O servidor verifica se o usuário já existe no sistema.
- Se o usuário já existir, o servidor envia uma resposta negativa.
- Caso contrário, o servidor cria o novo usuário e envia uma resposta positiva ao cliente.

### Registro de Acesso

- O servidor registra todas as tentativas de acesso em um arquivo de log. Isso inclui informações sobre data e hora, identificação da porta, identificação do usuário e se o acesso foi autorizado ou negado.

### Encerramento da Conexão

- Após lidar com uma solicitação de cliente, o servidor encerra a conexão com esse cliente específico.

## Para Pessoas Não Familiarizadas com o Projeto

Se você não estiver familiarizado com o projeto, aqui está uma explicação simplificada:

Imagine um sistema de controle de acesso em que várias portas precisam ser protegidas. Cada porta tem seu nível de segurança, e as pessoas que desejam entrar devem se autenticar com um nome de usuário e senha. As credenciais das pessoas são armazenadas em um banco de dados.

- O servidor é como um cérebro central que gerencia quem pode entrar e quem não pode.
- Quando alguém tenta entrar em uma porta, um cliente (um programa em um computador próximo à porta) se comunica com o servidor para verificar se a pessoa tem permissão.
- Se a pessoa tem permissão, a porta se abre; caso contrário, ela permanece fechada.
- O servidor mantém um registro de todas as tentativas de entrada, incluindo quem tentou entrar, quando e se foi permitido.
