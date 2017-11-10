# Trabalho 1 - Redes

#### Alunos:

#### Marcio Lima Inácio - 587265

#### Felipe Sampaio de Souza - 619523

----------

## Como executar

Para executar o programa, é necessário inicializar os `daemon.py` com acesso a portas específicas.

``` bash
python daemon.py -p 9001 &
python daemon.py -p 9002 &
python daemon.py -p 9003 &
```

Caso queira usar endereços e portas diferentes para cada máquina, é necessário alterar o dicionário `maq_addrs` em `backend.py`.

Com os _daemons_ executando, já é possível enviar a os comandos a serem executados a partir da página fornecida. É importante salientar que foram alterados os nomes de alguns campos do formulário presente na página por motivos de semântica, portanto é necessário utilizar a página fornecida neste projeto, na pasta `html`.