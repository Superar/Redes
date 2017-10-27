#!/usr/bin/python

import cgi
import cgitb
import subprocess
import re


result = list()
executaveis = ['ps', 'df', 'finger', 'uptime']
exec_list = list()

try:
    form = cgi.FieldStorage()
    form_str = '#'.join(form) + '#'
    regex = 'maq[1-3]_' + '(?:' + '|'.join(executaveis) + ')' + '(?=#)'

    # Encontra todos os comandos a serem executados
    exec_list = [elem.split('_') for elem in re.findall(regex, form_str)]

    for prog in exec_list:
        result.append(prog[0] + ' executando ' + prog[1])
        args = [prog[1]]  # Primeiro argumento precisa ser o nome do programa

        # Encontra os argumentos e insere na lista args
        args_key = prog[0] + '_' + prog[1]
        if args_key in form:
            args.append(tok for tok in form.getvalue(args_key).split(' '))

        # Cria subprocesso e executa
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        # Adiciona na lista de resultados o output
        for s in p.stdout.readlines():
            result.append(s)
        p.stdout.close()

except KeyError:
    print('Content-type:text/html')
    print
    print('<html><body> ERROR </body></html>')

else:
    print('Content-type:text/html')
    print
    print('<html>')
    if len(result) > 0:
        for s in result:
            print('<h1>%s</h1>' % s)
    else:
        print('<h1>Selecione algo</h1>')

    print('</html>')
