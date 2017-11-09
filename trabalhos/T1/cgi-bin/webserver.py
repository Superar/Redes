#!/usr/bin/python

import cgi
import cgitb
import subprocess
import re

send_backend = list()
executaveis = ['ps', 'df', 'finger', 'uptime']
exec_list = list()
result = list()

try:
    # Recupera as informacoes do form enviado
    form = cgi.FieldStorage()
    form_str = '#'.join(form) + '#'
    regex = 'maq[1-3]_' + '(?:' + '|'.join(executaveis) + ')' + '(?=#)'

    # Encontra todos os comandos a serem executados
    exec_list = [elem.split('_') for elem in re.findall(regex, form_str)]

    for prog in exec_list:
        args = prog  # Maquina e nome do programa

        # Encontra os argumentos e insere na lista args
        args_key = prog[0] + '_' + prog[1] + '_args'
        if args_key in form:
            args = args + form.getvalue(args_key).split(' ')

        send_backend.append(args)

    # Cria processo do backend
    p = subprocess.Popen(['python', 'backend.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    # Envia comandos no formato: maquina#comando#args
    for item in send_backend:
        p.stdin.write('#'.join(item))
        p.stdin.write('\n')
    p.stdin.close()

    # Recebe resposta do backend
    for s in p.stdout.readlines():
        result.append(s)
    p.stdout.close()

except Exception:
    print 'Content-type:text/html'
    print
    print '<html><body> ERROR </body></html>'

else:
    print 'Content-type:text/html'
    print
    print '<html>'
    if len(result) > 0:
        for s in result:
            print '%s' % s
    else:
        print '<h1>Selecione algo</h1>'

    print '</html>'
