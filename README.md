# Como executar
Há duas maneiras de executar o programa:
- Primeiro, acesse a pasta src.
- Depois use o comando main.py para acessar o programa através do CLI.

ou

- Primeiro, acesse a pasta src.
- use o comando main.py -gui para acessar o programa através da GUI.

O CLI faz o registro de produtos e fornecedores, lista-os e gera pedidos, validando os dados inseridos.
A GUI ainda está sendo construída. 
A janela para registro/listagem de produtos está quase pronta, faltando apenas a implementação da alteração de um produto. 
A janela de registro/listagem de fornecedores está sendo construida, ainda não efetua operações corretamente com excessão da listagem.
A janela para gerar pedidos ainda não foi feita.

O banco de dados é um arquivo JSON com 3 listas: produtos, fornecedores e pedidos. Há também a variável para controlar o id dos pedidos.