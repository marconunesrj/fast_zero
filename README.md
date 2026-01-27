## Para Chamar a Aplicação

- fastapi dev fast_zero/app.py (em modo Developer)
- fastapi run fast_zero/app.py (em modo de produção)
- uvicorn fast_zero.app:app
- task run --host 0.0.0.0

## pipx
O pipx é uma ferramenta usada para instalar e executar ferramentas Python globalmente no sistema de forma segura. Diferente do pip, que instala ferramentas sem um ambiente virtual (por padrão) e pode "sujar" nosso ambiente, o pipx cria um ambiente virtual e isola cada ferramenta dentro dele, facilitando a instalação de pacotes globais.

Em nosso projeto, usaremos o pipx para instalar ferramentas globais e executar algumas que serão usadas apenas uma vez.

Para instalar o pipx:

$ Execução no terminal!

pip install --user pipx
Dessa forma, a única dependência global que teremos no nosso sistema será o próprio pipx.

Existem outras formas de instalar o pipx
Caso você tenha um gerenciador de pacotes no seu sistema operacional, é extremamente recomendado que você instale o pipx por ele.

As instruções de instalação para cada sistema estão disponíveis na documentação do projeto.

Para o nosso sistema reconhecer o caminho das ferramentas instaladas via pipx podemos executar o comando:

$ Execução no terminal!

pipx ensurepath 
Esse comando adiciona ao PATH do sistema todos os binários instalados pelo pipx 🚨. Portanto, lembre-se de reiniciar o shell após executá-lo.

## Poetry
O Poetry é um gerenciador de projetos para Python. Ele pode nos ajudar em diversas etapas do ciclo de desenvolvimento, como a instalação de versões específicas do Python, a criação e manutenção de projetos (incluindo a definição de estruturas de pastas, o gerenciamento de ambientes virtuais e a instalação de bibliotecas), além de permitir a publicação de pacotes e muito mais.

No nosso projeto, ele será o componente central para agrupar e executar todas as tarefas relacionadas ao projeto.

Caso esse seja seu primeiro contato com o Poetry
Instalação do poetry
A instalação do Poetry pode ser feita de diversas maneiras, mas a forma que recomendo, para uma instalação global e isolada em um ambiente virtual, é via pipx:

$ Execução no terminal!

pipx install poetry 
Comentários em blocos
Blocos de código costumam ter comentários com informações adicionais, como este:

Ao clicar em  um bloco de comentário se abrirá, exibindo mais informações:



E, para facilitar nosso fluxo de trabalho com ambientes virtuais, vamos instalar uma extensão do Poetry para habilitar o shell:


via pipx
via poetry self
$ Execução no terminal!

pipx inject poetry poetry-plugin-shell 

Essa extensão adiciona o comando poetry shell, que habilita o ambiente virtual no terminal.

Gerenciamento de versões do Python
Após a instalação do Poetry, podemos utilizá-lo para gerenciar e instalar versões do Python que desejamos usar em um projeto. Para acompanhar este curso, a versão mínima do Python que você deve ter é a 3.11, pois alguns recursos que utilizaremos foram introduzidos nessa versão.

Você pode, no entanto, instalar qualquer versão mais nova. Minha recomendação é sempre que possível, use a versão mais atualizada possível:


Versão 3.14
Versão 3.13
Versão 3.12
Versão 3.11
Para utilizarmos uma versão específica do Python em nosso ambiente, devemos solicitar ao Poetry que instale essa versão:

$ Execução no terminal!

poetry python install 3.14  
Uma resposta similar a esta deve ser retornada ao executar o comando:

Resposta do comando `poetry python install`

Downloading and installing 3.14.0 (cpython) ... Done 
Testing 3.14.0 (cpython) ... Done

Dessa forma, garantimos que temos uma versão compatível do Python instalada.

Criando um projeto
Agora que temos o poetry e a versão do python que usaremos disponível, podemos iniciar a criação do nosso projeto. O primeiro passo é criar um novo projeto utilizando o Poetry, com o comando poetry new. Em seguida, navegaremos até o diretório criado:

$ Execução no terminal!

poetry new --flat fast_zero 
cd fast_zero
Ele criará uma estrutura de arquivos e pastas como essa:


.
├── fast_zero
│  └── __init__.py
├── pyproject.toml
├── README.md
└── tests
   └── __init__.py
Com a estrutura inicial do projeto criada e estando no diretório do projeto, podemos informar ao Poetry que queremos usar a versão do Python que instalamos. Para isso, utilizamos o seguinte comando:


Versão 3.13
Versão 3.12
Versão 3.11
$ Execução no terminal!

poetry env use 3.13
Em conjunto com essa instrução, devemos também especificar no Poetry que usaremos exatamente a versão 3.13 em nosso projeto. Para isso, alteramos o arquivo de configuração pyproject.toml na raiz do projeto:

pyproject.toml

[project]
# ...
requires-python = ">=3.13,<4.0" 

Dessa forma, garantimos que o Poetry usará a versão correta do Python ao criar o ambiente virtual para o nosso projeto.

Instalando o FastAPI
Com toda a base do nosso projeto pronta, podemos finalmente instalar o FastAPI:

$ Execução no terminal!

poetry install 
poetry add 'fastapi[standard]' 

## Dica: Como abrir o terminal interativo (REPL)
Para apenas chamar o terminal interativo: python -i
Para abrir o terminal interativo com o seu código carregado, você deve chamar o Python no terminal usando -i:

$ Execução no terminal!

python -i <seu_arquivo.py>
O interpretador do Python executa o código do arquivo e retorna o shell após executar tudo que está escrito no arquivo.

Para o nosso caso específico, como o nome do arquivo é fast_zero/app.py, devemos executar esse comando no terminal:

$ Execução no terminal!

python -i fast_zero/app.py

## Instalando as ferramentas de desenvolvimento
As escolhas de ferramentas de desenvolvimento, de forma geral, são escolhas bem particulares. Não costumam ser consensuais nem mesmo em times de desenvolvimento. Dito isso, selecionei algumas ferramentas que gosto de usar e alinhadas com a utilidade que elas apresentam no desenvolvimento do projeto.

As ferramentas escolhidas são:

- taskipy: ferramenta usada para criação de comandos. Como executar a aplicação, rodar os testes, etc.
- pytest: ferramenta para escrever e executar testes
- ruff: Uma ferramenta que tem duas funções no nosso - - - código:
Um analisador estático de código (um linter), para dizer se não estamos infringindo alguma boa prática de programação;
Um formatador de código. Para seguirmos um estilo único de código. Vamos nos basear na PEP-8.
Para instalar essas ferramentas que usaremos em desenvolvimento, podemos usar um grupo de dependências (--group dev no poetry) focado nelas, para não serem instaladas quando nossa aplicação estiver em produção:

$ Execução no terminal!

poetry add --group dev pytest pytest-cov taskipy ruff


## Utilizando o Task

- task lint
- task format
- task test
- task post_test - Mesmo se der erro se executar este comando ele gera o relatório de cobertura

Criando o arquivo .gitignore

Vamos iniciar com a criação de um arquivo .gitignore específico para Python. Existem diversos modelos disponíveis na internet, como os disponíveis pelo próprio GitHub, ou o gitignore.io. Uma ferramenta útil é a ignr, feita em Python, que faz o download automático do arquivo para a nossa pasta de trabalho atual:

$ Execução no terminal!

- pipx run ignr -p python > .gitignore 

Criando um repositório no github ( Eu crio primeiro no git hub e depois executos os comandos abaixo, se der erro chamo o Copilot)

Agora, com nossos arquivos indesejados ignorados, podemos iniciar o versionamento de código usando o git. Para criar um repositório local, usamos o comando git init .. Para criar esse repositório no GitHub, utilizaremos o gh, um utilitário de linha de comando que nos auxilia nesse processo:

$ Execução no terminal!

- git init
- git add .
- git commit -m "Configuração inicial do projeto"
- git push --set-upstream origin main


Descobrindo o seu endereço local usando python
Caso não esteja familiarizado com o terminal ou ferramentas para descobrir seu endereço IP:

- Chamando o Terminal interativo!
python -i 

>>> import socket
>>> s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
>>> s.connect(("8.8.8.8", 80))
>>> s.getsockname()[0]
'192.168.0.100'


## Incluir pydantic-settings
Para gerenciar e separar nossas configurações do código de forma segura e estruturada, usaremos o pydantic-settings. Essa biblioteca permite que você defina configurações tanto em variáveis de ambiente quanto em arquivos separados (como .env), evitando a escrita de configurações diretamente no código-fonte.

$ Execução no terminal!

poetry add pydantic-settings

## Incluir SqlAlchemy
Agora que entendemos melhor esses conceitos, começaremos instalando o SQLAlchemy, um ORM que nos permite trabalhar com bancos de dados SQL de maneira Pythonica. Além disso, o Alembic, que é uma ferramenta de migração de banco de dados, funciona muito bem com o SQLAlchemy e nos ajudará a gerenciar as alterações do esquema do nosso banco de dados.

$ Execução no terminal!

poetry add sqlalchemy

# Referência do SqlAlchemy

- https://docs.sqlalchemy.org/en/20/
- https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column


## Instalando o Alembic e Criando a Primeira Migração
instalando o Alembic, que é uma ferramenta de migração de banco de dados para SQLAlchemy. Usaremos o Poetry para adicionar o Alembic ao nosso projeto:

$ Execução no terminal!

poetry add alembic

Após a instalação do Alembic, precisamos iniciá-lo em nosso projeto. O comando de inicialização criará um diretório migrations e um arquivo de configuração alembic.ini:

$ Execução no terminal!

alembic init migrations

# Para criar a migração, utilizamos o seguinte comando:

$ Execução no terminal!

alembic revision --autogenerate -m "create users table"

## Comandos Alembic

- alembic history
- alembic upgrade head
- alembic downgrade -1
- downgrade base
- alembic upgrade +1

# Acessar o console do sqlite e verificar. Precisamos chamar sqlite3 nome_do_arquivo.db:

Caso não tenha o SQLite instalado na sua máquina:
Arch
pacman -S sqlite

Debian/Ubuntu
sudo apt install sqlite3

Mac
brew install sqlite

Windows
winget install --id SQLite.SQLite

$ Execução no terminal!

sqlite3 database.db
