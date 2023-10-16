# Sistema de Controle de Acesso - Especificação de Projeto

## Visão Geral

Este projeto consiste na implementação de uma aplicação de controle de acesso, composta por um servidor central e vários clientes distribuídos em portas. O sistema permite monitorar a entrada e saída de pessoas em um ambiente, exigindo autenticação por nome de usuário e credenciais (senha). O acesso é concedido com base na correspondência das credenciais do usuário com as informações armazenadas em um banco de dados.

## Funcionalidades

### Lado Cliente

O cliente é instalado em cada porta e desempenha as seguintes funções:

1. Ler as informações fornecidas pelo usuário através do teclado.
2. Enviar os dados fornecidos para o servidor.
3. Receber as informações de autorização do servidor.
4. Imprimir a resposta do servidor na tela.

### Lado Servidor

O servidor é instalado na central de controle do ambiente e realiza as seguintes tarefas:

1. Armazenar as credenciais dos usuários em uma base de dados.
2. Receber solicitações de cadastro de novas credenciais de usuário.
3. Receber requisições enviadas pelos clientes.
4. Consultar a base de dados de usuários para autenticação.
5. Registrar as tentativas de acesso em um arquivo de registro.
6. Enviar informações de autorização para os clientes.

### Credenciais do Usuário

As credenciais dos usuários são armazenadas em um arquivo TXT, com cada linha contendo as seguintes informações:

- Código do usuário.
- Nome do usuário.
- Nível de acesso.

Exemplo:

```
1458, Elend Venture, 5
4287, Edgard Ladrian, 4
4298, Vin, 2
6528, Lord Renoux, 3
7458, Kelsier, 1
```

- Usuários com nível de acesso 1 podem acessar apenas a sala 1.
- Usuários com nível de acesso 2 podem acessar as salas 1 e 2.
- Usuários com nível de acesso 5 podem acessar todas as salas.

### Arquivo de Registro

O arquivo de registro de tentativas de acesso é um arquivo no formato TXT. Cada tentativa de acesso relatada pelos clientes é registrada em uma linha deste arquivo. Cada linha do arquivo contém as seguintes informações:

- Data e hora no formato dd/mm/aaaa - hh:mm:ss.
- Identificação da porta.
- Identificação do usuário.
- Autorização (autorizado ou negado).

Exemplo:

```
04/09/2018 – 13:20:14, p1, 1458, autorizado
04/09/2018 – 14:11:35, p2, 7458, negado
```

### Protocolo

Um protocolo de comunicação é definido para controlar as trocas de mensagens entre clientes e servidores. Ele leva em consideração situações como perda de conexão, perda de pacotes e define os seguintes parâmetros de aplicação:

1. Formato das mensagens: O formato das mensagens deve seguir um padrão específico, detalhado abaixo.
2. Comportamento em caso de perda de conexão ou pacotes: Define como o sistema lida com a perda de conexão ou pacotes durante a comunicação.
3. Encerramento de conexões: Especifica quando as conexões devem ser encerradas, tanto no cliente quanto no servidor.

## Formato das Mensagens

O formato das mensagens deve incluir informações essenciais para a autenticação e autorização, como:

- Identificação da porta.
- Nome do usuário.
- Credenciais do usuário.
- Resposta de autorização.

## Executando

O código pode ser executado com qualquer interpretador de python3.x sem a necessidade de qualquer biblioteca adicional.

Para executar o servidor, basta executar o arquivo `server.py` estando dentro da pasta `server`:

```bash
python3 server.py
```

Para executar o cliente, basta executar o arquivo `client.py` estando dentro da pasta `client`:

```bash
python3 client.py
```