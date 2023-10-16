# Funcionamento dos Módulos `door.py` e `user.py`

Os módulos `door.py` e `user.py` são componentes essenciais da aplicação de controle de acesso. Eles definem classes e funcionalidades relacionadas a portas (doors) e usuários (users). Abaixo, explicaremos o funcionamento de cada um desses módulos e como eles operam.

## `door.py`

### Classe `Door`

A classe `Door` representa uma porta no sistema de controle de acesso. Cada porta tem um ID exclusivo e um nível de autenticação que define o quão segura é. Aqui está o funcionamento da classe `Door`:

- **Constructor (`__init__`)**: O construtor da classe recebe um ID de porta e um nível de autenticação (padrão: 0). Ele inicializa os atributos `id` e `authentication_level`.

- **`__str__`**: Este método fornece uma representação em string da porta, incluindo seu ID e nível de autenticação.

- **`have_access`**: Este método permite verificar se um usuário tem acesso a uma porta específica com base no nível de autenticação do usuário. Se o nível de autenticação do usuário for maior do que o nível de autenticação da porta, o método retorna `True`, indicando que o acesso é permitido.

### Classe `Doors`

A classe `Doors` gerencia um conjunto de portas no sistema de controle de acesso. Ela pode carregar portas de um arquivo de banco de dados (padrão: "doors.csv"), adicionar novas portas, recuperar portas por ID e salvar portas no banco de dados. Aqui está o funcionamento da classe `Doors`:

- **Constructor (`__init__`)**: O construtor recebe o nome do arquivo de banco de dados (padrão: "doors.csv") e inicializa o atributo `database`. Em seguida, ele chama o método `load` para carregar as portas do arquivo de banco de dados.

- **`__str__`**: Este método fornece uma representação em string de todas as portas gerenciadas pela classe.

- **`add_door`**: Este método permite adicionar uma nova porta ao conjunto de portas gerenciado pela classe. Ele verifica se a porta já existe no conjunto antes de adicioná-la.

- **`get_door`**: Este método permite recuperar uma porta com base em seu ID. Se a porta existir, ele retorna a instância da porta; caso contrário, retorna `None`.

- **`load`**: Este método carrega as portas do arquivo de banco de dados especificado. Ele verifica se o arquivo existe e, se não existir, cria um novo arquivo vazio. Em seguida, lê as portas do arquivo e as adiciona ao conjunto de portas gerenciado pela classe.

- **`save`**: Este método salva todas as portas no banco de dados. Ele escreve as portas no arquivo especificado.

## `user.py`

### Classe `User`

A classe `User` representa um usuário no sistema de controle de acesso. Cada usuário tem um nome de usuário, uma senha e um nível de autenticação. Aqui está o funcionamento da classe `User`:

- **Constructor (`__init__`)**: O construtor da classe recebe um nome de usuário, uma senha e um nível de autenticação (padrão: 0). Ele inicializa os atributos `username`, `password` e `authentication_level`.

- **`__str__`**: Este método fornece uma representação em string do usuário, incluindo seu nome de usuário, senha e nível de autenticação.

- **`have_access`**: Este método permite verificar se um usuário tem acesso com base em seu nível de autenticação. Se o nível de autenticação do usuário for maior do que o nível de autenticação especificado, o método retorna `True`, indicando que o acesso é permitido.

- **`login`**: Este método permite que o usuário faça login no sistema. Ele recebe uma senha como entrada e verifica se a senha corresponde à senha armazenada para o usuário. Se a senha estiver correta, o método retorna `True`, indicando que o login foi bem-sucedido.

### Classe `Users`

A classe `Users` gerencia um conjunto de usuários no sistema de controle de acesso. Ela pode carregar usuários de um arquivo de banco de dados (padrão: "users.csv"), adicionar novos usuários, recuperar usuários por nome de usuário, remover usuários e salvar usuários no banco de dados. Aqui está o funcionamento da classe `Users`:

- **Constructor (`__init__`)**: O construtor recebe o nome do arquivo de banco de dados (padrão: "users.csv") e inicializa o atributo `database`. Em seguida, ele chama o método `load_users` para carregar os usuários do arquivo de banco de dados.

- **`__str__`**: Este método fornece uma representação em string de todos os usuários gerenciados pela classe.

- **`add_user`**: Este método permite adicionar um novo usuário ao conjunto de usuários gerenciado pela classe. Ele verifica se o usuário já existe no conjunto antes de adicioná-lo e, em seguida, chama o método `save_users` para atualizar o banco de dados.

- **`get_user`**: Este método permite recuperar um usuário com base em seu nome de usuário. Se o usuário existir, ele retorna a instância do usuário; caso contrário, retorna `None`.

- **`remove_user`**: Este método permite remover um usuário do conjunto de usuários gerenciado pela classe. Ele atualiza o banco de dados após a remoção.

- **`load_users`**: Este método carrega os usuários do arquivo de banco de dados especificado. Ele verifica se o arquivo existe e, se não existir, cria um novo arquivo vazio. Em seguida, lê os usuários do arquivo e os adiciona ao conjunto de usuários gerenciado pela classe.

- **`save_users`**: Este método salva todos os usuários no banco de dados. Ele escreve os usuários no arquivo especificado.

- **`login`**: Este método permite que um usuário faça login no sistema. Ele recebe um nome de usuário e uma senha como entrada, verifica se o usuário existe e, em seguida, chama o método `login` da classe `User` para verificar a senha.

- **`have_access`**: Este método permite verificar se um usuário tem acesso com base em seu nome de usuário e nível de autenticação. Ele chama o método `have_access` da classe `User` para realizar a verificação.

Esses módulos `door.py` e `user.py` fornecem as estruturas de dados e funcionalidades necessárias para gerenciar portas e usuários no sistema de controle de acesso. Eles são essenciais para garantir que o sistema funcione corretamente ao verificar credenciais e autorizações.