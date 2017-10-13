#!/usr/bin/python

import cgi, cgitb 
import subprocess


result = []

try:
	form = cgi.FieldStorage()
	
	maq1_ps = form.getvalue('maq1_ps')
	valor = form.getvalue('maq1-ps')
	p = subprocess.Popen(['ps'], stdout=subprocess.PIPE)
	for s in p.stdout.readlines():
		result.append(s)
	p.stdout.close()
except KeyError:
	print 'Content-type:text/html'
	print
	print "<html><body> ERROR </body></html>"
else:
	print 'Content-type:text/html'
	print
	print '<html>'
	if maq1_ps:
		print '<h1>Selecionado: %s</h1>' % maq1_ps
		for s in result:
			print '<h1>%s</h1>' % s

	else:
		print '<h1>Selecione algo</h1>'
	print '</html>'
