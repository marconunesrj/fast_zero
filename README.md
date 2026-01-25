## Para Chamar a Aplicação

fastapi dev fast_zero/app.py (em modo Developer)
fastapi run fast_zero/app.py (em modo de produção)
uvicorn fast_zero.app:app

## Instalando as ferramentas de desenvolvimento
As escolhas de ferramentas de desenvolvimento, de forma geral, são escolhas bem particulares. Não costumam ser consensuais nem mesmo em times de desenvolvimento. Dito isso, selecionei algumas ferramentas que gosto de usar e alinhadas com a utilidade que elas apresentam no desenvolvimento do projeto.

As ferramentas escolhidas são:

taskipy: ferramenta usada para criação de comandos. Como executar a aplicação, rodar os testes, etc.
pytest: ferramenta para escrever e executar testes
ruff: Uma ferramenta que tem duas funções no nosso código:
Um analisador estático de código (um linter), para dizer se não estamos infringindo alguma boa prática de programação;
Um formatador de código. Para seguirmos um estilo único de código. Vamos nos basear na PEP-8.
Para instalar essas ferramentas que usaremos em desenvolvimento, podemos usar um grupo de dependências (--group dev no poetry) focado nelas, para não serem instaladas quando nossa aplicação estiver em produção:

$ Execução no terminal!

poetry add --group dev pytest pytest-cov taskipy ruff


## Utilizando o Task

task lint
task format
task test
task post_test - Mesmo se der erro se executar este comando ele gera o relatório de cobertura

Criando o arquivo .gitignore

Vamos iniciar com a criação de um arquivo .gitignore específico para Python. Existem diversos modelos disponíveis na internet, como os disponíveis pelo próprio GitHub, ou o gitignore.io. Uma ferramenta útil é a ignr, feita em Python, que faz o download automático do arquivo para a nossa pasta de trabalho atual:

$ Execução no terminal!

pipx run ignr -p python > .gitignore 

Criando um repositório no github

Agora, com nossos arquivos indesejados ignorados, podemos iniciar o versionamento de código usando o git. Para criar um repositório local, usamos o comando git init .. Para criar esse repositório no GitHub, utilizaremos o gh, um utilitário de linha de comando que nos auxilia nesse processo:

$ Execução no terminal!

git init .
$ Instalar o gh, eu instalei pelo Chocolatei, depois de instalar tem que fechar o terminal e criar outro
choco install gh
gh repo create
Ao executar gh repo create, algumas informações serão solicitadas, como o nome do repositório e se ele será público ou privado. Isso irá criar um repositório tanto localmente quanto no GitHub.

Subindo nosso código para o github

Com o repositório pronto, vamos versionar nosso código. Primeiro, adicionamos o código ao próximo commit com git add .. Em seguida, criamos um ponto na história do projeto com git commit -m "Configuração inicial do projeto". Por fim, sincronizamos o repositório local com o remoto no GitHub usando git push:

$ Execução no terminal!

git add .
git commit -m "Configuração inicial do projeto"
git push
