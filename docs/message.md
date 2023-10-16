# Funcionamento do Protocolo de Mensagens

O protocolo de mensagens implementado no arquivo `message.py` permite a comunicação entre o servidor e os clientes na aplicação de controle de acesso. Ele define a estrutura das mensagens trocadas entre as partes e fornece métodos para serializar, enviar, receber e desserializar essas mensagens.

## Estrutura das Mensagens

As mensagens no protocolo têm a seguinte estrutura:

- **Tipo de Mensagem (`type`)**: Um valor enumerado que indica o tipo de mensagem. Os tipos de mensagem suportados são `LOGIN` (0) e `SIGNUP` (1), que representam as operações de login e registro, respectivamente.

- **ID (`id`)**: Um número inteiro de 4 bits (0 a 15) que identifica a mensagem. Cada mensagem enviada pelo cliente tem um ID exclusivo para que o servidor possa corresponder as respostas às solicitações originais.

- **Timestamp (`timestamp`)**: Um carimbo de data e hora representado como um número inteiro de 64 bits que indica o momento em que a mensagem foi criada.

- **Autorização (`authorized`)**: Um valor booleano que indica se a operação (login ou registro) foi autorizada ou não.

- **Nome de Usuário (`username`)**: Uma string de até 50 caracteres que contém o nome de usuário fornecido pelo cliente.

- **Senha (`password`)**: Uma senha representada como uma string de 4 dígitos (0 a 9999) fornecida pelo cliente.

## Funcionamento do Protocolo

### 1. Criação de Mensagem

O cliente cria uma instância da classe `Message` com os parâmetros necessários, como tipo de mensagem, ID, nome de usuário, senha e timestamp. A mensagem é criada usando o construtor da classe `Message`.

### 2. Serialização da Mensagem

A mensagem é serializada em bytes usando o método `pack` da classe `Message`. A serialização segue o seguinte formato:

- O tipo de mensagem (`type`) e o ID (`id`) são compactados em um único byte.
- O timestamp (`timestamp`) é serializado como um número longo (64 bits).
- O nome de usuário (`username`) é serializado como uma string de até 50 caracteres.
- A senha (`password`) é serializada como uma string de 4 dígitos.

A mensagem serializada é então enviada para o servidor.

### 3. Envio da Mensagem

A mensagem serializada é enviada pelo cliente para o servidor por meio de uma conexão de soquete (socket). Isso é feito usando o método `send` da classe `Message`, que envia os bytes serializados para o servidor.

### 4. Recebimento de Resposta

O servidor recebe a mensagem, processa-a e envia uma resposta de volta para o cliente. O cliente aguarda a resposta do servidor após o envio da mensagem.

### 5. Recebimento da Resposta

O cliente usa o método `receive` da classe `Message` para receber a resposta do servidor. Este método aguarda a resposta do servidor e a desserializa de bytes para uma instância da classe `Message`.

### 6. Desserialização da Resposta

A resposta do servidor é desserializada usando o método `unpack` da classe `Message`. Isso envolve a extração do tipo de mensagem, ID, timestamp, autorização, nome de usuário e senha da mensagem serializada recebida do servidor.

### 7. Processamento da Resposta

O cliente processa a resposta do servidor para determinar se a operação foi autorizada ou não. Ele usa as informações de autorização e outros detalhes fornecidos na resposta para tomar decisões e informar o usuário.

### 8. Encerramento da Comunicação

Após o processamento da resposta, a comunicação entre o cliente e o servidor pode continuar com outras operações ou ser encerrada, dependendo do fluxo da aplicação.

Este protocolo de mensagens permite que o cliente e o servidor comuniquem-se de forma estruturada e eficiente, trocando informações relevantes para as operações de login e registro, bem como outros aspectos da aplicação de controle de acesso. A estrutura e a validação das mensagens garantem a integridade e a segurança da comunicação entre as partes.