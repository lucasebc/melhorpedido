# Como executar
Através do terminal (Com duplo clique o python não responde adequadamente)
- Primeiro, acesse a pasta src.
- Depois use o comando "main.py" para acessar o programa através do CLI.

# Como executar a GUI
A GUI foi feita usando o QT. Portanto, é necessário instalar o módulo QT para executar.
- Primeiro, use o comando "pip install pyside2".
- Então, acesse a pasta src e execute o comando "main.py -gui" para acessar o programa através da GUI.

Através da interface gráfica é possível cadastrar, alterar, excluir e listar produtos e "fornecedores".
Para pedidos é possível apenas gerar novos pedidos até o momento.

O banco de dados é um arquivo JSON com 3 listas: produtos, fornecedores e pedidos. Há também a variável para controlar o id dos pedidos.
