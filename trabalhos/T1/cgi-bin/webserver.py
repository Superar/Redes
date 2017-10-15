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

    for executavel in executaveis:
        comandos = re.findall('maq[1-3]_' + executavel + '#', '#'.join(form))
        for elem in comandos:
            exec_list.append(elem[:-1].split('_'))

    for prog in exec_list:
        result.append(prog[0] + ' executando ' + prog[1])
        args = [prog[1]]

        if prog[0] + '_' + prog[1] + '_args' in form:
            for tok in form.getvalue(prog[0] + '_' + prog[1] + '_args').split(' '):
                args.append(tok)

        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        for s in p.stdout.readlines():
            result.append(s)
        p.stdout.close()

except KeyError:
    print 'Content-type:text/html'
    print
    print '<html><body> ERROR </body></html>'

else:
    print 'Content-type:text/html'
    print
    print '<html>'
    if len(result) > 0:
        for s in result:
            print '<h1>%s</h1>' % s
    else:
        print '<h1>Selecione algo</h1>'

    print '</html>'
